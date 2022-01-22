<?php

	$data_msg = "";

?>
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>Iran access</title>
</head>

<body>

	<?php

		if(isset($_POST['submit'])) {
			$username = $_POST['username'];
			$password = $_POST['password'];
			$address = $_POST['address'];
			$type_access = $_POST['type_access'];

			if($type_access == "empty") {
				$data_msg = "please select type iran access";
			} elseif($type_access == "yes") {
				if(!$username) {
					$data_msg = "please insert username";
				} elseif(!$password) {
					$data_msg = "please insert password";
				} elseif(!$address) {
					$data_msg = "please insert ip address";
				} else {
					exec("bash add-remove.sh $username $password $address yes", $data_exec);
				}
			} elseif($type_access == "no") {
				if(!$username) {
					$data_msg = "please insert username";
				} elseif(!$password) {
					$data_msg = "please insert password";
				} elseif(!$address) {
					$data_msg = "please insert ip address";
				} else {
					exec("bash add-remove.sh $username $password $address no", $data_exec);
				}
			} elseif($type_access == "listips") {
				if(!$username) {
					$data_msg = "please insert username";
				} elseif(!$password) {
					$data_msg = "please insert password";
				} else {
					exec("bash showips.sh $username $password", $data_exec);
				}
			}

		}

	?>

	<form method="post" action="" enctype="multipart/form-data">
		<table border="0">
			<tr>
				<td>username :</td>
				<td><input type="text" name="username" style="width:200px;" /></td>
			</tr>
			<tr>
				<td>password :</td>
				<td><input type="text" name="password" style="width:200px;" /></td>
			</tr>
			<tr>
				<td>ip address :</td>
				<td><input type="text" name="address" style="width:200px;" /></td>
			</tr>
			<tr>
				<td>type :</td>
				<td>
					<select name="type_access" style="width:200px;">
						<option value="empty">----</option>
						<option value="yes">yes, iran access</option>
						<option value="no">no, iran access</option>
						<option value="listips">show list ip iran access</option>
					</select>
				</td>
			</tr>
			<tr>
				<td></td>
				<td><input type="submit" name="submit" /></td>
			</tr>
		</table>
	</form>
	
	
	<?php print $data_msg; ?>
	
	
	<?php 
	echo "<pre>";
	print_r($data_exec);
	echo "</pre>";
	?>



</body>
</html>


