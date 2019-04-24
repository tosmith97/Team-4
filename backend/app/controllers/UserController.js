const authService = require('./../services/AuthService');

exports.authUser = async function (req, res) {
    const authCode = req.params.authorizationCode;

    if (!authCode) return ReE(res, {error: 'Missing auth code'}, 400);
    authService.authUser(authCode);

    return ReS(res, {success: true}, 200);
}


exports.mockGoogleLogin = async function (req, res) {
    authService.mockOAuth();
    return ReS(res, {success: true}, 200);
}

exports.googleAuthCallback = async function (req, res) {
    const authCode = req.query.code; 
    if (!authCode) return ReE(res, {message: 'failed to get auth code'}, 400);
    
    let err, _;
    [err, _] = await to(authService.authUser(authCode));
    if (err) return ReE(res, err, 500);

    return ReS(res, {success: true}, 200);
}

