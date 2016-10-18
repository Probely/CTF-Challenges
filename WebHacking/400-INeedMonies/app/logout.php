<?php
require 'confs.php';
session_destroy();
header('Location: login.php');
