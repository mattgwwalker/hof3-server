divert(-1)dnl This diverts the output to a non-existant stream (like /dev/null) 

dnl htmlHeader takes two parameters:
dnl The first is the title of the page
dnl The second is the id prefix
dnl
dnl The function writes out the boilerplate header requires for jQuery
dnl Mobile.  After calling this function, htmlHeaderEnd should be called
dnl to terminate the elements opened by htmlHeader.
define(`htmlHeader',`dnl
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HT5ML//EN">
<html>
<head>
  <title>$1</title>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="css/custom.css" />
  <link rel="stylesheet" href="css/default-plus-f.min.css" />
  <link rel="stylesheet" href="css/jquery.mobile.structure-1.3.2.css" />
  <script src="js/jquery-1.9.1.js"></script>
  <script src="js/jquery.mobile-1.3.2.js"></script>
  <script src="js/flot/jquery.flot.js"></script>
  <script src="js/flot/jquery.flot.time.js"></script>

dnl These scripts should be turned into one file to enhance loading times.
  <script src="js_src/production.js"></script>
  <script src="js_src/debug.js"></script>

</head>

<body>
<div data-role="page" id="$2">

<div data-role="header" id="$2-Header">
  <h1>$1</h1>
</div>

<div data-role="popup" id="$2-ErrorPopup" data-theme="e">
  <div data-role="header" data-theme="e">
    <h1 id="$2-ErrorPopupTitle">Error</h1>
  </div>
  <div data-role="content" id="$2-ErrorPopupText" data-theme="e">
  </div>
</div>  

<div data-role="content" id="$2-Content">
  <div id="$2-Message" class="ui-body ui-body-e" style="display:none;">
  </div>


<!-- End of boilerplate -->
')


dnl htmlHeaderEnd takes no parameters and closes the elements opened
dnl by htmlHeader.
define(`htmlHeaderEnd',`dnl
<!-- Start of terminating boilerplate -->

</div> <!-- End of "content"-->

</div> <!-- End of "page"-->
</body>
</html>
')


divert(1)dnl Return to outputting to standard out.
