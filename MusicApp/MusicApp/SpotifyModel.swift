//
//  SpotifyModel.swift
//  MusicApp
//
//  Created by Joshua Singer on 4/17/19.
//  Copyright © 2019 Joshua Singer. All rights reserved.
//

import RealmSwift



class MusicLoggedin: Object {
    @objc dynamic var spotifyLoggedIn = false
    @objc dynamic var soundcloudLoggedIn = false
}

