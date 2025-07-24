# stream_socket_client - php_network_getaddresses: getaddrinfo failed: Name or service not known
[Link to question](https://stackoverflow.com/questions/33566084/stream-socket-client-php-network-getaddresses-getaddrinfo-failed-name-or-ser)
**Creation Date:** 1446810286
**Score:** 1
**Tags:** php, sockets, drupal, server, ubuntu-14.04
## Question Body
<pre><code>function drupal_http_request($url, array $options = array()) {
  // Allow an alternate HTTP client library to replace Drupal's default
  // implementation.
  $override_function = variable_get('drupal_http_request_function', FALSE);
  if (!empty($override_function) &amp;&amp; function_exists($override_function)) {
    return $override_function($url, $options);
  }

  $result = new stdClass();

  // Parse the URL and make sure we can handle the schema.
  $uri = @parse_url($url);

  if ($uri == FALSE) {
    $result-&gt;error = 'unable to parse URL';
    $result-&gt;code = -1001;
    return $result;
  }

  if (!isset($uri['scheme'])) {
    $result-&gt;error = 'missing schema';
    $result-&gt;code = -1002;
    return $result;
  }

  timer_start(__FUNCTION__);

  // Merge the default options.
  $options += array(
    'headers' =&gt; array(),
    'method' =&gt; 'GET',
    'data' =&gt; NULL,
    'max_redirects' =&gt; 3,
    'timeout' =&gt; 30.0,
    'context' =&gt; NULL,
  );

  // Merge the default headers.
  $options['headers'] += array(
    'User-Agent' =&gt; 'Drupal (+http://drupal.org/)',
  );

  // stream_socket_client() requires timeout to be a float.
  $options['timeout'] = (float) $options['timeout'];

  // Use a proxy if one is defined and the host is not on the excluded list.
  $proxy_server = variable_get('proxy_server', '');
  if ($proxy_server &amp;&amp; _drupal_http_use_proxy($uri['host'])) {
    // Set the scheme so we open a socket to the proxy server.
    $uri['scheme'] = 'proxy';
    // Set the path to be the full URL.
    $uri['path'] = $url;
    // Since the URL is passed as the path, we won't use the parsed query.
    unset($uri['query']);

    // Add in username and password to Proxy-Authorization header if needed.
    if ($proxy_username = variable_get('proxy_username', '')) {
      $proxy_password = variable_get('proxy_password', '');
      $options['headers']['Proxy-Authorization'] = 'Basic ' . base64_encode($proxy_username . (!empty($proxy_password) ? ":" . $proxy_password : ''));
    }
    // Some proxies reject requests with any User-Agent headers, while others
    // require a specific one.
    $proxy_user_agent = variable_get('proxy_user_agent', '');
    // The default value matches neither condition.
    if ($proxy_user_agent === NULL) {
      unset($options['headers']['User-Agent']);
    }
    elseif ($proxy_user_agent) {
      $options['headers']['User-Agent'] = $proxy_user_agent;
    }
  }

  switch ($uri['scheme']) {
    case 'proxy':
      // Make the socket connection to a proxy server.
      $socket = 'tcp://' . $proxy_server . ':' . variable_get('proxy_port', 8080);
      // The Host header still needs to match the real request.
      $options['headers']['Host'] = $uri['host'];
      $options['headers']['Host'] .= isset($uri['port']) &amp;&amp; $uri['port'] != 80 ? ':' . $uri['port'] : '';
      break;

    case 'http':
    case 'feed':
      $port = isset($uri['port']) ? $uri['port'] : 80;
      $socket = 'tcp://' . $uri['host'] . ':' . $port;
      // RFC 2616: "non-standard ports MUST, default ports MAY be included".
      // We don't add the standard port to prevent from breaking rewrite rules
      // checking the host that do not take into account the port number.
      $options['headers']['Host'] = $uri['host'] . ($port != 80 ? ':' . $port : '');
      break;

    case 'https':
      // Note: Only works when PHP is compiled with OpenSSL support.
      $port = isset($uri['port']) ? $uri['port'] : 443;
      $socket = 'ssl://' . $uri['host'] . ':' . $port;
      $options['headers']['Host'] = $uri['host'] . ($port != 443 ? ':' . $port : '');
      break;

    default:
      $result-&gt;error = 'invalid schema ' . $uri['scheme'];
      $result-&gt;code = -1003;
      return $result;
  }

  if (empty($options['context'])) {
    $fp = @stream_socket_client($socket, $errno, $errstr, $options['timeout']);
  }
  else {
    // Create a stream with context. Allows verification of a SSL certificate.
    $fp = @stream_socket_client($socket, $errno, $errstr, $options['timeout'], STREAM_CLIENT_CONNECT, $options['context']);
  }
  var_dump($fp);

  // Make sure the socket opened properly.
  if (!$fp) {
    // When a network error occurs, we use a negative number so it does not
    // clash with the HTTP status codes.
    $result-&gt;code = -$errno;
    $result-&gt;error = trim($errstr) ? trim($errstr) : t('Error opening socket @socket', array('@socket' =&gt; $socket));
    print_r($result);
    exit();

    // Mark that this request failed. This will trigger a check of the web
    // server's ability to make outgoing HTTP requests the next time that
    // requirements checking is performed.
    // See system_requirements().
    variable_set('drupal_http_request_fails', TRUE);

    return $result;
  }

  // Construct the path to act on.
  $path = isset($uri['path']) ? $uri['path'] : '/';
  if (isset($uri['query'])) {
    $path .= '?' . $uri['query'];
  }

  // Only add Content-Length if we actually have any content or if it is a POST
  // or PUT request. Some non-standard servers get confused by Content-Length in
  // at least HEAD/GET requests, and Squid always requires Content-Length in
  // POST/PUT requests.
  $content_length = strlen($options['data']);
  if ($content_length &gt; 0 || $options['method'] == 'POST' || $options['method'] == 'PUT') {
    $options['headers']['Content-Length'] = $content_length;
  }

  // If the server URL has a user then attempt to use basic authentication.
  if (isset($uri['user'])) {
    $options['headers']['Authorization'] = 'Basic ' . base64_encode($uri['user'] . (isset($uri['pass']) ? ':' . $uri['pass'] : ':'));
  }

  // If the database prefix is being used by SimpleTest to run the tests in a copied
  // database then set the user-agent header to the database prefix so that any
  // calls to other Drupal pages will run the SimpleTest prefixed database. The
  // user-agent is used to ensure that multiple testing sessions running at the
  // same time won't interfere with each other as they would if the database
  // prefix were stored statically in a file or database variable.
  $test_info = &amp;$GLOBALS['drupal_test_info'];
  if (!empty($test_info['test_run_id'])) {
    $options['headers']['User-Agent'] = drupal_generate_test_ua($test_info['test_run_id']);
  }

  $request = $options['method'] . ' ' . $path . " HTTP/1.0\r\n";
  foreach ($options['headers'] as $name =&gt; $value) {
    $request .= $name . ': ' . trim($value) . "\r\n";
  }
  $request .= "\r\n" . $options['data'];
  $result-&gt;request = $request;
  // Calculate how much time is left of the original timeout value.
  $timeout = $options['timeout'] - timer_read(__FUNCTION__) / 1000;
  if ($timeout &gt; 0) {
    stream_set_timeout($fp, floor($timeout), floor(1000000 * fmod($timeout, 1)));
    fwrite($fp, $request);
  }

  // Fetch response. Due to PHP bugs like http://bugs.php.net/bug.php?id=43782
  // and http://bugs.php.net/bug.php?id=46049 we can't rely on feof(), but
  // instead must invoke stream_get_meta_data() each iteration.
  $info = stream_get_meta_data($fp);
  $alive = !$info['eof'] &amp;&amp; !$info['timed_out'];
  $response = '';

  while ($alive) {
    // Calculate how much time is left of the original timeout value.
    $timeout = $options['timeout'] - timer_read(__FUNCTION__) / 1000;
    if ($timeout &lt;= 0) {
      $info['timed_out'] = TRUE;
      break;
    }
    stream_set_timeout($fp, floor($timeout), floor(1000000 * fmod($timeout, 1)));
    $chunk = fread($fp, 1024);
    $response .= $chunk;
    $info = stream_get_meta_data($fp);
    $alive = !$info['eof'] &amp;&amp; !$info['timed_out'] &amp;&amp; $chunk;
  }
  fclose($fp);

  if ($info['timed_out']) {
    $result-&gt;code = HTTP_REQUEST_TIMEOUT;
    $result-&gt;error = 'request timed out';
    return $result;
  }
  // Parse response headers from the response body.
  // Be tolerant of malformed HTTP responses that separate header and body with
  // \n\n or \r\r instead of \r\n\r\n.
  list($response, $result-&gt;data) = preg_split("/\r\n\r\n|\n\n|\r\r/", $response, 2);
  $response = preg_split("/\r\n|\n|\r/", $response);

  // Parse the response status line.
  $response_status_array = _drupal_parse_response_status(trim(array_shift($response)));
  $result-&gt;protocol = $response_status_array['http_version'];
  $result-&gt;status_message = $response_status_array['reason_phrase'];
  $code = $response_status_array['response_code'];

  $result-&gt;headers = array();

  // Parse the response headers.
  while ($line = trim(array_shift($response))) {
    list($name, $value) = explode(':', $line, 2);
    $name = strtolower($name);
    if (isset($result-&gt;headers[$name]) &amp;&amp; $name == 'set-cookie') {
      // RFC 2109: the Set-Cookie response header comprises the token Set-
      // Cookie:, followed by a comma-separated list of one or more cookies.
      $result-&gt;headers[$name] .= ',' . trim($value);
    }
    else {
      $result-&gt;headers[$name] = trim($value);
    }
  }

  $responses = array(
    100 =&gt; 'Continue',
    101 =&gt; 'Switching Protocols',
    200 =&gt; 'OK',
    201 =&gt; 'Created',
    202 =&gt; 'Accepted',
    203 =&gt; 'Non-Authoritative Information',
    204 =&gt; 'No Content',
    205 =&gt; 'Reset Content',
    206 =&gt; 'Partial Content',
    300 =&gt; 'Multiple Choices',
    301 =&gt; 'Moved Permanently',
    302 =&gt; 'Found',
    303 =&gt; 'See Other',
    304 =&gt; 'Not Modified',
    305 =&gt; 'Use Proxy',
    307 =&gt; 'Temporary Redirect',
    400 =&gt; 'Bad Request',
    401 =&gt; 'Unauthorized',
    402 =&gt; 'Payment Required',
    403 =&gt; 'Forbidden',
    404 =&gt; 'Not Found',
    405 =&gt; 'Method Not Allowed',
    406 =&gt; 'Not Acceptable',
    407 =&gt; 'Proxy Authentication Required',
    408 =&gt; 'Request Time-out',
    409 =&gt; 'Conflict',
    410 =&gt; 'Gone',
    411 =&gt; 'Length Required',
    412 =&gt; 'Precondition Failed',
    413 =&gt; 'Request Entity Too Large',
    414 =&gt; 'Request-URI Too Large',
    415 =&gt; 'Unsupported Media Type',
    416 =&gt; 'Requested range not satisfiable',
    417 =&gt; 'Expectation Failed',
    500 =&gt; 'Internal Server Error',
    501 =&gt; 'Not Implemented',
    502 =&gt; 'Bad Gateway',
    503 =&gt; 'Service Unavailable',
    504 =&gt; 'Gateway Time-out',
    505 =&gt; 'HTTP Version not supported',
  );
  // RFC 2616 states that all unknown HTTP codes must be treated the same as the
  // base code in their class.
  if (!isset($responses[$code])) {
    $code = floor($code / 100) * 100;
  }
  $result-&gt;code = $code;

  switch ($code) {
    case 200: // OK
    case 304: // Not modified
      break;
    case 301: // Moved permanently
    case 302: // Moved temporarily
    case 307: // Moved temporarily
      $location = $result-&gt;headers['location'];
      $options['timeout'] -= timer_read(__FUNCTION__) / 1000;
      if ($options['timeout'] &lt;= 0) {
        $result-&gt;code = HTTP_REQUEST_TIMEOUT;
        $result-&gt;error = 'request timed out';
      }
      elseif ($options['max_redirects']) {
        // Redirect to the new location.
        $options['max_redirects']--;
        $result = drupal_http_request($location, $options);
        $result-&gt;redirect_code = $code;
      }
      if (!isset($result-&gt;redirect_url)) {
        $result-&gt;redirect_url = $location;
      }
      break;
    default:
      $result-&gt;error = $result-&gt;status_message;
  }

  return $result;
}
</code></pre>

<p>I'm getting the below mentioned message by doing <code>var_dump</code> of <code>$fp</code> as mentioned above on my <code>VM machine</code> hosted with <code>Ubuntu 14.04</code></p>

<pre><code>stdClass Object
(
    [code] =&gt; 0
    [error] =&gt; php_network_getaddresses: getaddrinfo failed: Name or service not known
)
</code></pre>

<p>When I'm implementing the same thing on my <code>localhost</code> which is <code>XAMPP</code> based in <code>Windows 7</code> I'm getting this:</p>

<pre><code>Resource id #8
</code></pre>

<p>Due to this I'm unable to use the <a href="https://api.drupal.org/api/drupal/includes%21common.inc/function/drupal_http_request/7" rel="nofollow">drupal_http_request</a></p>

<p>As per your suggestion I've tried <code>dns_get_record()</code></p>

<pre><code>$dns_get_record = dns_get_record("www.google.com");
print_r($dns_get_record);
</code></pre>

<p>and got this as the output:</p>

<pre><code>Array
(
    [0] =&gt; Array
        (
            [host] =&gt; www.google.com
            [class] =&gt; IN
            [ttl] =&gt; 243
            [type] =&gt; A
            [ip] =&gt; 216.58.220.4
        )

    [1] =&gt; Array
        (
            [host] =&gt; www.google.com
            [class] =&gt; IN
            [ttl] =&gt; 257
            [type] =&gt; AAAA
            [ipv6] =&gt; 2404:6800:4009:805::2004
        )

)
</code></pre>

<p>I've also checked the <code>stream_socket_client()</code></p>

<pre><code>var_dump(stream_socket_client());
</code></pre>

<p>and it returned me <code>bool(false)</code></p>

## Answers
### Answer ID: 33567908
<p>Since you've not put any proper error handling in the code, we can't tell which function is being executed. You haven't provided the parameters you are passing, so we can't tell what the cause is, but the most likely issue is that you are trying to establish a network connection and the host where the code is running is unable to resolve the hostname inside $socket.</p>

<p>You can very this with dns_get_record() or speak to your hosting provider.</p>

