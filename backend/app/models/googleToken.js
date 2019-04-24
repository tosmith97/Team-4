const mongoose = require('mongoose');

const GoogleTokenSchema = mongoose.Schema({
    _userId: { type: mongoose.Schema.Types.ObjectId, required: true, ref: 'User' },
    access_token: {
        type: String,
        required: true
    },
    refresh_token: {
        type: String,
        required: true
    },
    id_token:  {
        type: String,
        required: true
    },
    scope:  {
        type: String,
        required: true
    },
    createdAt: { type: Date, required: true, default: Date.now, expires: 43200 }
});


const GoogleToken = mongoose.model('GoogleToken', GoogleTokenSchema);
module.exports = GoogleToken;