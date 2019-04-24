//
//  ViewController.swift
//  MusicApp
//
//  Created by Joshua Singer on 3/24/19.
//  Copyright © 2019 Joshua Singer. All rights reserved.
//

import UIKit
import GoogleSignIn

class LoginSignUpViewController: UIViewController, GIDSignInUIDelegate {

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        
        GIDSignIn.sharedInstance().uiDelegate = self
        
        // Uncomment to automatically sign in the user.
        //GIDSignIn.sharedInstance().signInSilently()
        
        // TODO(developer) Configure the sign-in button look/feel
        // ...
    }

    func sign(_ signIn: GIDSignIn?, didSignInFor user: GIDGoogleUser?) throws {
        let idToken = user?.authentication.idToken
    }
    
    
    
    
}

