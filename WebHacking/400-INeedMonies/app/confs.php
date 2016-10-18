<?php

# enable errors (debug only)
error_reporting(E_ALL);
ini_set("display_errors", 0);

# use composer
require_once '../vendor/autoload.php';

# configure twig
$loader = new Twig_Loader_Filesystem('../templates');
$twig = new Twig_Environment($loader, array(
));

define("VICTIM_USER", "bruce@shaydmail.org");
define("ATTACKER_USER", "nakemeigbo1@sapo.pt");
define("ATTACKER_PASS", "h9AvhRDPDKSfxpBqfMer9FzD");
define("INITIAL_BALANCE", 530);
define("TARGET_BALANCE", 1000000);
define("VICTIM_INITIAL_BALANCE", 1000000);
define("FLAG", 1195254);
define("INTERNAL_ENDPOINT", "localhost");

# start session
session_start();

define("LOGGED_IN", isset($_SESSION['username']) && !empty($_SESSION['username']));
