<?php
require 'confs.php';

if (!LOGGED_IN) {
    header('Location: login.php');
}

$error = <<<EOF
Error near line 20:

if (!account->get(\$from)) {
   throw new Exception('Invalid account');
}

// transfer between 2 accounts
\$endpoint .= "/transfer.php?from=\$from&to=\$to&amount=\$amount&id=\$id";

EOF;

if (isset($_POST['xml']) && !empty($_POST['xml'])) {

	syslog(LOG_WARNING, "XML payload: {$_SERVER['REMOTE_ADDR']} \"{$_SERVER['HTTP_USER_AGENT']}\" {$_POST['xml']}");

   	$tooMaliciousPayload = 0;

    $whitelistEntity = '/ENTITY[\s%]+[\w-\.:]+\s+SYSTEM\s+["\'](\w+):\/\//';
	$hits = preg_match_all($whitelistEntity, $_POST['xml'], $matches,  PREG_PATTERN_ORDER);
	for ($i=0; $tooMaliciousPayload == 0 && $i < $hits; $i++) {
		if (strtolower($matches[1][$i]) != "http" &&
			strtolower($matches[1][$i]) != "https") {
				$tooMaliciousPayload = 1;
		}
	}
	
    $whitelistPublic = '/ENTITY\s+[\w-\.:]+\s+PUBLIC\s+["\'].+?["\']\s+["\'](\w+):\/\//';
	$hits = preg_match_all($whitelistPublic, $_POST['xml'], $matches,  PREG_PATTERN_ORDER);
	for ($i=0; $tooMaliciousPayload == 0 && $i < $hits; $i++) {
		if (strtolower($matches[1][$i]) != "http" &&
			strtolower($matches[1][$i]) != "https") {
				$tooMaliciousPayload = 1;
		}
	}
	
	if ($tooMaliciousPayload == 1) {			
		// if it has entity it can only be http or https
        echo "transfer failed: denied";
    } else {
		$old_balance = $_SESSION['balance'];
				
		// Unlock session cookie to prevent deadlocks
        session_write_close();
		
		foreach(array('file') as $wrap) {
			stream_wrapper_unregister($wrap);
		}

        $dom = new DOMDocument;       
        if (!$dom->loadXML($_POST['xml'], LIBXML_NOENT)) {
            // an attack was tried
            echo $error;
        } else {
            $list = $dom->getElementsByTagName('to');
            foreach ($list as $node) {
                $to = $node->nodeValue;
                break;
            }
            $list = $dom->getElementsByTagName('from');
            foreach ($list as $node) {
                $from = $node->nodeValue;
                break;
            }
            $list = $dom->getElementsByTagName('amount');
            foreach ($list as $node) {
                $amount = $node->nodeValue;
                break;
            }
            $list = $dom->getElementsByTagName('id');
            foreach ($list as $node) {
                $id = $node->nodeValue;
                break;
            }

            if (intval($amount) > $old_balance) {
                echo "transfer failed: insufficient funds";
            } else if ($from != ATTACKER_USER) {
                echo "transfer failed: invalid account";
            } else if (intval($amount) > 0) {
                $curl = curl_init();

                curl_setopt_array($curl, array(
                    CURLOPT_RETURNTRANSFER => 1,
                    CURLOPT_URL => "http://".INTERNAL_ENDPOINT."/transfer.php?from=".$from."&to=".$to."&amount=".$amount."&id=".$id
                ));

                $resp = curl_exec($curl);
                curl_close($curl);

                if ($resp == "OK") {
                    echo "success. Refresh to update your balance";
                } else {
                    echo "transfer failed: endpoint returned NOK";
                }
            } else {
                echo "transfer failed: invalid amount";
            }
        }
    }
}
