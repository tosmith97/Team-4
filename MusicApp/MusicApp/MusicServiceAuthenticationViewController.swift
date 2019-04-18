//
//  MusicServiceAuthenticationViewController.swift
//  MusicApp
//
//  Created by Joshua Singer on 3/24/19.
//  Copyright © 2019 Joshua Singer. All rights reserved.
//

import UIKit

class MusicServiceAuthenticationViewController: UIViewController {
    
    let SpotifyClientID = "31f86341f7554668966e8a1b983c16ab"
    let SpotifyRedirectURL = URL(string: "musicapp://spotify-login-callback")!
    let delegate = UIApplication.shared.delegate as! AppDelegate

    lazy var configuration = SPTConfiguration(
        clientID: SpotifyClientID,
        redirectURL: SpotifyRedirectURL
    )
    
   
   
    @IBOutlet weak var spotifyAuthenticationButton: UIButton!
    
    
    @IBOutlet weak var soundcloudAuthenticationButton: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()

        // Do any additional setup after loading the view.
    }
    
    @IBAction func authenticateSpotifyPressed(_ sender: Any) {
        let requestedScopes: SPTScope = [.appRemoteControl]
        delegate.sessionManager.initiateSession(with: requestedScopes, options: .default)



    }
    
    
    @IBAction func authenticateSoundCloudPressed(_ sender: Any) {
    }
    
    
    
    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
