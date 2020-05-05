<?php

  // I use https://cron-job.org/en/ to execute this regularly
  // Setup: need to create two files: next_ponder_month.txt (with content: Month,YYYY) and last_jane_street_title.txt (leave empty) for this work.
  
  $my_email = 'my@mail.com'; // fill in your own email address

  echo '<html>';
    
	// check for new Jane Street Puzzle
	$html = file_get_contents("https://www.janestreet.com/puzzles/current-puzzle/");
	$current_puzzle_title_p1 = explode('<span class="puzzle-post-title">', $html);
	$current_puzzle_title_p2 = explode('</span>', $current_puzzle_title_p1[1]);
	$current_puzzle_title = $current_puzzle_title_p2[0];
	// retrieve last title and compare
	$myfile = fopen("last_jane_street_title.txt", "r") or die("Unable to open file!");
	$last_title = fgets($myfile);
	fclose($myfile);
	if ($current_puzzle_title == $last_title) {
		echo '<p>No new Jane Street Puzzle</p>';
	} else {
		echo '<p>There is a New Jane Street Puzzle</p>';
		$to      = $my_email;
		$subject = 'There is a new Jane Street Puzzle';
		$message = ' Check it out: https://www.janestreet.com/puzzles/current-puzzle/';
	
		$headers .= "Reply-To: Walter Sebastian Gisler <".$my_email."\r\n";
		$headers .= "Return-Path: Walter Sebastian Gisler <".$my_email.">\r\n";
		$headers .= "From: Walter Sebastian Gisler <".$my_email.">\r\n";
		$headers .= "Organization: GotSoccer\r\n";
		$headers .= "MIME-Version: 1.0\r\n";
		$headers .= "Content-type: text/plain; charset=iso-8859-1\r\n";
		$headers .= "X-Priority: 3\r\n";
		$headers .= "X-Mailer: PHP" . phpversion() . "\r\n";
	
		mail($to, $subject, $message, $headers);
		file_put_contents('last_jane_street_title.txt', $current_puzzle_title);
	}
	
	
	
	// check for new IBM Ponder challenge
	$myfile = fopen("next_ponder_month.txt", "r") or die("Unable to open file!");
	$next_month = fgets($myfile);
	$nm = $bodytag = str_replace(",", "", $next_month);
	fclose($myfile);
	$html = file_get_contents("http://www.research.ibm.com/haifa/ponderthis/challenges/".$nm.".html");
	$s = strpos($html , 'Challenge');
    if($s) { 
        echo "<p>There is a new IBM Ponder challenge: <a href='http://www.research.ibm.com/haifa/ponderthis/challenges/".$nm.".html'>Link</a></p>";
        $to      = $my_email;
		$subject = 'There is a new IBM Ponder Challenge';
		$message = ' Check it out: http://www.research.ibm.com/haifa/ponderthis/challenges/'.$nm.'.html';
	
		$headers .= "Reply-To: Walter Sebastian Gisler <".$my_email.">\r\n";
		$headers .= "Return-Path: Walter Sebastian Gisler <".$my_email.">\r\n";
		$headers .= "From: Walter Sebastian Gisler <".$my_email.">\r\n";
		$headers .= "Organization: The Puzzle Organization\r\n";
		$headers .= "MIME-Version: 1.0\r\n";
		$headers .= "Content-type: text/plain; charset=iso-8859-1\r\n";
		$headers .= "X-Priority: 3\r\n";
		$headers .= "X-Mailer: PHP" . phpversion() . "\r\n";
	
		mail($to, $subject, $message, $headers);
		
        $month_year = explode(',', $next_month);
        $month = $month_year[0];
        $year = $month_year[1];
        $nexty = $year;
        if($month == 'January') {
            $nextm = 'February';
        }
        if($month == 'February') {
            $nextm = 'March';
        }
        if($month == 'March') {
            $nextm = 'April';
        }
        if($month == 'April') {
            $nextm = 'May';
        }
        if($month == 'May') {
            $nextm = 'June';
        }
        if($month == 'June') {
            $nextm = 'July';
        }
        if($month == 'July') {
            $nextm = 'August';
        }
        if($month == 'August') {
            $nextm = 'September';
        }
        if($month == 'September') {
            $nextm = 'October';
        }
        if($month == 'October') {
            $nextm = 'November';
        }
        if($month == 'November') {
            $nextm = 'December';
        }
        if($month == 'December') {
            $nextm = 'January';
            $nexty = ((int)$year)+1;
        }
        file_put_contents('next_ponder_month.txt', $nextm.",".$nexty);
    }
    else {
        echo "<p>There is no new IBM Ponder challenge: http://www.research.ibm.com/haifa/ponderthis/challenges/".$nm.".html</p>";
    }
	echo '</html>';
?>
