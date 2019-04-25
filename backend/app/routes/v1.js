const express 			= require('express');
const router 			= express.Router();

const MainController 	= require('./../controllers/MainController');
const SpotifyController 	= require('./../controllers/SpotifyController');
const UserController 	= require('./../controllers/UserController');


/* GET home page. */
router.get('/', function(req, res, next) {
  res.json({status:"success", message:"Parcel Pending API", data:{"version_number":"v1.0.0"}})
});


/*
  GET Request
  localhost:8000/v1/dummy
  Sample request:
*/
router.get('/dummy',           MainController.dummyFunction);

/*
  Endpoints for Spotify Authorization
*/
router.get('/spotifyLogin',         SpotifyController.loginFunction);
router.get('/spotifyLoginCallback', SpotifyController.loginCallback);

router.get('/mockGoogleLogin', UserController.mockGoogleLogin);
router.get('/googleAuthCallback', UserController.googleAuthCallback);


module.exports = router;
