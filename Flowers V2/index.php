<?php
highlight_file(__FILE__); echo ($data = @json_decode(@file_get_contents($_POST['url']))) ? $data->message : 'pu71n';
?>
