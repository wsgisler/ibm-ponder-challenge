from docplex.mp.model import Model as MipModel
from itertools import combinations
from random import random

def main():
    # data
    orchids = [1,2,3,4]
    days = [1,2,3]
    barrels = ['A','B','C','D','E','F','G','H','I','J','K','L']
    
    model = MipModel("ponder_january_2020")
    
    variables = {(orchid, day, barrel): model.binary_var(name = 'O%d_D%d_B%s'%(orchid, day, barrel)) for orchid in orchids for day in days for barrel in barrels}
    
    combs = list(combinations(barrels, 2))
    
    die = {(orchid, day, comb): model.binary_var(name = 'O%d_D%d_B%s'%(orchid, day, str(comb))) for orchid in orchids for day in days for comb in combs}
    doesnt_die = {(orchid, comb): model.binary_var(name = 'ddO%d_B%s'%(orchid, str(comb))) for orchid in orchids for comb in combs}
    multipliers = {(orchid, day): random() for orchid in orchids for day in days}
    
    # An orchid can die at most once:
    for orchid in orchids:
        for comb in combs:
            model.add(model.sum(die[(orchid, day, comb)] for day in days)+doesnt_die[(orchid, comb)] == 1)
    
    for poison_barrels in combs:
        for orchid in orchids:
            for day in days:
                for barrel in barrels:
                    model.add(variables[(orchid, day, barrel)]*(1 if barrel in poison_barrels else 0) <= model.sum(die[(orchid, d2, poison_barrels)] for d2 in [1,2,3] if d2 <= day))
                model.add(model.sum(variables[(orchid, day, barrel)] for barrel in barrels if barrel in poison_barrels) >= die[(orchid, day, poison_barrels)])
            #model.add(1-model.sum(variables[(orchid, day, barrel)] for day in days for barrel in barrels if barrel in poison_barrels) >= doesnt_die[(orchid, poison_barrels)])
                
    # At least one and at most 3 barrels per rose per day
    for orchid in orchids:
        for day in days:
            model.add(model.sum(variables[(orchid, day, barrel)] for barrel in barrels) >= 1)
            model.add(model.sum(variables[(orchid, day, barrel)] for barrel in barrels) <= 3)
            
    # If a barrel has been used already for a rose, don't use it again
    for orchid in orchids:
        for barrel in barrels:
            model.add(1-variables[(orchid, 1, barrel)] >= variables[(orchid, 2, barrel)])
            model.add(1-variables[(orchid, 1, barrel)] >= variables[(orchid, 3, barrel)])
            model.add(1-variables[(orchid, 2, barrel)] >= variables[(orchid, 3, barrel)])
    
    # Every combination should have a different fingerprint
    for comb_1 in combs:
        for comb_2 in combs:
            if comb_1 != comb_2:
                decider = model.binary_var()
                model.add(model.sum(die[(orchid, day, comb_1)]*multipliers[(orchid, day)] for orchid in orchids for day in days) >= 
                          0.01+model.sum(die[(orchid, day, comb_2)]*multipliers[(orchid, day)] for orchid in orchids for day in days)-decider*1000)
                model.add(0.01+model.sum(die[(orchid, day, comb_1)]*multipliers[(orchid, day)] for orchid in orchids for day in days)-(1-decider)*1000 <= 
                          model.sum(die[(orchid, day, comb_2)]*multipliers[(orchid, day)] for orchid in orchids for day in days))

    model.parameters.threads = 16
    model.parameters.timelimit = 20000
    solution = model.solve(log_output = True)
    model.export_as_lp('model.lp')
    
    for key in variables:
        if variables[key].solution_value >= 0.5:
            print(key)
            
    for comb in combs:
        print(comb)
        for orchid in orchids:
            for day in days:
                if die[(orchid, day, comb)].solution_value > 0.5:
                    print('Orchid '+str(orchid)+' will die on day '+str(day))
    print(multipliers)

if __name__ == "__main__":
    main()
