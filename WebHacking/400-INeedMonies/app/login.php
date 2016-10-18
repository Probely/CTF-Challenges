<?php
require 'confs.php';

if (LOGGED_IN) {
    header('Location: account.php');
    die();
}

$msg = "";
if (isset($_POST['username']) && !empty($_POST['username']) &&
    isset($_POST['password']) && !empty($_POST['password'])) {

    if ($_POST['username'] === ATTACKER_USER &&
        $_POST['password'] === ATTACKER_PASS) {
        $_SESSION['username'] = $_POST['username'];
        $_SESSION['balance'] = INITIAL_BALANCE;
		$_SESSION['victim_balance'] = VICTIM_INITIAL_BALANCE;
        header('Location: account.php');
    } else if (preg_match('/\'/', $_POST['username'])){
    	include("c5_67t3qguywhdqoy8guhaw.html");
    } else {
        $msg = "Wrong username or password";
    }
} elseif (array_key_exists('username', $_POST) || array_key_exists('password', $_POST)) {
    $msg = "Enter your username and password";
}
echo $twig->render('login.html', array('errormsg' => $msg, 'username' => isset($_POST['username']) ? $_POST['username'] : ""));
