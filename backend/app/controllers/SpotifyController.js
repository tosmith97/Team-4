const querystring = require('querystring');
const request = require('request');

var stateKey = 'spotify_auth_state';
var redirect_uri = 'http://localhost:' + CONFIG.port + '/v1/spotifyLoginCallback';

var generateRandomString = function(length) {
  var text = '';
  var possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

  for (var i = 0; i < length; i++) {
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  }
  return text;
};

/**
 * Note: this endpoint is for *~testing purposes only~*
 * Login flow will start from iOS side and use the callback endpoint below
 */
exports.loginFunction = function (req, res) {
  var state = generateRandomString(16);
  res.cookie(stateKey, state);

  // Request authorization
  var scope = 'user-read-private user-read-email user-modify-playback-state user-read-playback-state user-top-read';
  res.redirect('https://accounts.spotify.com/authorize?' +
    querystring.stringify({
      response_type: 'code',
      client_id: KEYS.client_id,
      scope: scope,
      redirect_uri: redirect_uri,
      state: state
    }));
}

/**
 * Requests authorization from Spotify API and
 * sends access_token, refresh_token, timeout
 * TODO: replace redirects with proper error handling 
 */
exports.loginCallback = function (req, res) {

  var code = req.query.code || null;
  var state = req.query.state || null;
  var storedState = req.cookies ? req.cookies[stateKey] : null;

  if (state === null || state !== storedState) {
    res.redirect('/#' +
      querystring.stringify({
        error: 'state_mismatch'
      }));
  } else {
    res.clearCookie(stateKey);
    var authOptions = {
      url: 'https://accounts.spotify.com/api/token',
      form: {
        code: code,
        redirect_uri: redirect_uri,
        grant_type: 'authorization_code'
      },
      headers: {
        'Authorization': 'Basic ' + (new Buffer(KEYS.client_id+':'+KEYS.client_secret).toString('base64'))
      },
      json: true
    };

    request.post(authOptions, function(error, response, body) {
      if (!error && response.statusCode === 200) {
        var access_token = body.access_token,
            refresh_token = body.refresh_token,
            expires_in = body.expires_in;

        var user_options = {
          url: 'https://api.spotify.com/v1/me',
          headers: { 'Authorization': 'Bearer ' + access_token },
          json: true
        };

        res.send({
          'access_token': access_token,
          'refresh_token': refresh_token,
          'timeout': expires_in
        });
      } else {
        res.redirect('/#' +
          querystring.stringify({
            error: 'invalid_token'
          }));
      }
    });
  }
}
