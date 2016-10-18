<?php

// Set the session_id before everything
session_id($_GET['id']);
require '../app/confs.php';

if (isset($_GET['to']) && !empty($_GET['to']) &&
    isset($_GET['from']) && !empty($_GET['from']) &&
    isset($_GET['amount']) && !empty($_GET['amount']) &&
    isset($_GET['id']) && !empty($_GET['id'])) {

    if (!LOGGED_IN) {
        echo "NOK";
        die();
    }

    if ($_GET['to'] == ATTACKER_USER &&
        $_GET['from'] == VICTIM_USER &&
        intval($_GET['amount']) > 0 &&
		intval($_GET['amount']) <= $_SESSION['victim_balance']) {
        echo "OK";
        $_SESSION['balance'] += intval($_GET['amount']);
		$_SESSION['victim_balance'] -= intval($_GET['amount']);
    } else if ($_GET['to'] == VICTIM_USER &&
        $_GET['from'] == ATTACKER_USER &&
        intval($_GET['amount']) > 0 &&
		intval($_GET['amount']) <= $_SESSION['balance']) {
        echo "OK";
        $_SESSION['balance'] -= intval($_GET['amount']);
		$_SESSION['victim_balance'] += intval($_GET['amount']);
    } else {
        echo "NOK";
    }
} else {
    echo "NOK";
}
