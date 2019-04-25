const User = require('./../models').User;
const GoogleToken = require('./../models').GoogleToken;

const {google} = require('googleapis');

const redirect_uri = 'http://localhost:' + CONFIG.port + '/v1/googleAuthCallback';

const oauth2Client = new google.auth.OAuth2(
    CONFIG.google_oauth_client_id,
    CONFIG.google_oauth_client_secret,
    redirect_uri
);


// oauth2client.on('tokens', (tokens) => {
//     if (tokens.refresh_token) {
//         // store the refresh_token in my database!
//         console.log(tokens.refresh_token);
//     }
//     console.log(tokens.access_token);
// });

// *** This will be handled client-side ***
exports.mockOAuth = async function () {
    const SCOPES = [
        'https://www.googleapis.com/auth/userinfo.email',
        'https://www.googleapis.com/auth/userinfo.profile'
    ];

    const url = oauth2Client.generateAuthUrl({
        access_type: 'offline',
        scope: SCOPES,
    });

    console.info(`authUrl: ${url}`);
}


exports.authUser = async function (code) {
    const {tokens} = await oauth2Client.getToken(code);
    oauth2Client.setCredentials(tokens);
    let googleToken = {
        access_token: tokens.access_token,
        refresh_token: tokens.refresh_token,
        id_token: tokens.id_token,
        scope: tokens.scope
    }

    const people = google.people({
        version: 'v1',
        auth: oauth2Client,
    });

    const res = await people.people.get({
        resourceName: 'people/me',
        personFields: 'emailAddresses,names',
    });

    const name = res.data.names[0].displayName;
    const email = res.data.emailAddresses[0].value;
    
    let err, oldUser;
    [err, oldUser] = await to(User.findOne({
        'email': email
    }));
    if (oldUser) {
        googleToken._userId = oldUser.id;

        // Update token
        let token;
        [err, token] = await to(GoogleToken.findOneAndReplace(
            { _userId: oldUser.id },
            { googleToken },
            { upsert: true }
        ));

        if (err) TE(err.message);
    }

    // create new user
    userInfo = { name, email };

    let newUser, token;
    [err, newUser] = await to(User.create(userInfo));
    if (err) TE(err.message);
    googleToken._userId = newUser.id;

    [err, token] = await to(GoogleToken.create(googleToken)); 
    if (err) TE(err.message);

}