<?php
require 'confs.php';
if (LOGGED_IN) {
    header('Location: account.php');
} else {
    header('Location: login.php');
}
