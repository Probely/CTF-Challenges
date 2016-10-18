<?php
require 'confs.php';

if (!LOGGED_IN) {
    header('Location: login.php');
    die();
}

if ($_SESSION['balance'] >= TARGET_BALANCE && $_SESSION['balance'] < FLAG) {
	$_SESSION['balance'] = FLAG;
}

echo $twig->render('account.html', array(
    'session' => $_SESSION,
    'session_id' => session_id()));
