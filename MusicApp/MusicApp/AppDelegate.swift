//
//  AppDelegate.swift
//  MusicApp
//
//  Created by Joshua Singer on 3/24/19.
//  Copyright © 2019 Joshua Singer. All rights reserved.
//

import UIKit
import GoogleSignIn




@UIApplicationMain
class AppDelegate: UIResponder, UIApplicationDelegate, GIDSignInDelegate, SPTSessionManagerDelegate {
    
    let SpotifyClientID = "31f86341f7554668966e8a1b983c16ab"
    let SpotifyRedirectURL = URL(string: "musicapp://spotify-login-callback")!
    
    lazy var configuration = SPTConfiguration(
        clientID: SpotifyClientID,
        redirectURL: SpotifyRedirectURL
    )
    
    

    lazy var sessionManager: SPTSessionManager = {
        if let tokenSwapURL = URL(string: "https://[your token swap app domain here]/api/token"),
            let tokenRefreshURL = URL(string: "https://[your token swap app domain here]/api/refresh_token") {
            self.configuration.tokenSwapURL = tokenSwapURL
            self.configuration.tokenRefreshURL = tokenRefreshURL
            self.configuration.playURI = ""
        }
        let manager = SPTSessionManager(configuration: self.configuration, delegate: self)
        return manager
    }()

    
    func sessionManager(manager: SPTSessionManager, didInitiate session: SPTSession) {
        print("success", session)
    }
    func sessionManager(manager: SPTSessionManager, didFailWith error: Error) {
        print("fail", error)
    }
    func sessionManager(manager: SPTSessionManager, didRenew session: SPTSession) {
        print("renewed", session)
    }
    
    
    
    
    
    func sign(_ signIn: GIDSignIn!, didSignInFor user: GIDGoogleUser!,
              withError error: Error!) {
        if let error = error {
            print("\(error.localizedDescription)")
        } else {
            // Perform any operations on signed in user here.
            let userId = user.userID                  // For client-side use only!
            let idToken = user.authentication.idToken // Safe to send to the server
            let fullName = user.profile.name
            let givenName = user.profile.givenName
            let familyName = user.profile.familyName
            let email = user.profile.email
            // ...
            
            print("\(fullName) is logged in")
            let activityStoryboard = UIStoryboard(name: "Main", bundle: nil)
            let vc = activityStoryboard.instantiateViewController(withIdentifier: "MusicServiceAuthViewController")
            window?.rootViewController = vc
            window?.makeKeyAndVisible()

//            // Access the storyboard and fetch an instance of the view controller
//            let storyboard = UIStoryboard(name: "Main", bundle: nil);
//            let viewController: MusicServiceAuthenticationViewController = storyboard.instantiateViewController(withIdentifier: "MusicServiceAuthViewController") as! MusicServiceAuthenticationViewController
//
//            // Then push that view controller onto the navigation stack
//            let rootViewController = self.window!.rootViewController as! LoginSignUpViewController;
//            rootViewController.pushViewController(viewController, animated: true);
        }
    }
    
    func sign(_ signIn: GIDSignIn!, didDisconnectWith user: GIDGoogleUser!,
              withError error: Error!) {
        GIDSignIn.sharedInstance().signOut()
        

        // Perform any operations when the user disconnects from app here.
        // ...
    }

    

    var window: UIWindow?


    func application(_ application: UIApplication, didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
        // Override point for customization after application launch.
        
        // Initialize sign-in
        GIDSignIn.sharedInstance().clientID = "340602704654-th8ut6t82i0jmi1goq04l5bgiakmdktr.apps.googleusercontent.com"
        GIDSignIn.sharedInstance().delegate = self

        return true
    }

    func applicationWillResignActive(_ application: UIApplication) {
        // Sent when the application is about to move from active to inactive state. This can occur for certain types of temporary interruptions (such as an incoming phone call or SMS message) or when the user quits the application and it begins the transition to the background state.
        // Use this method to pause ongoing tasks, disable timers, and invalidate graphics rendering callbacks. Games should use this method to pause the game.
    }

    func applicationDidEnterBackground(_ application: UIApplication) {
        // Use this method to release shared resources, save user data, invalidate timers, and store enough application state information to restore your application to its current state in case it is terminated later.
        // If your application supports background execution, this method is called instead of applicationWillTerminate: when the user quits.
    }

    func applicationWillEnterForeground(_ application: UIApplication) {
        // Called as part of the transition from the background to the active state; here you can undo many of the changes made on entering the background.
    }

    func applicationDidBecomeActive(_ application: UIApplication) {
        // Restart any tasks that were paused (or not yet started) while the application was inactive. If the application was previously in the background, optionally refresh the user interface.
    }

    func applicationWillTerminate(_ application: UIApplication) {
        // Called when the application is about to terminate. Save data if appropriate. See also applicationDidEnterBackground:.
    }
    
    func application(_ app: UIApplication, open url: URL, options: [UIApplication.OpenURLOptionsKey : Any] = [:]) -> Bool {
        
        
        let sendingAppID = options[.sourceApplication]
        print("source application = \(sendingAppID ?? "Unknown") sending app")
        print("\(sendingAppID)")
        if "\(sendingAppID ?? "Unknown")" == "com.spotify.client" {
            self.sessionManager.application(app, open: url, options: options)
            print("here")
            return true
        }
        
        
        return GIDSignIn.sharedInstance().handle(url as URL?,
                                                 sourceApplication: options[UIApplication.OpenURLOptionsKey.sourceApplication] as? String,
                                                 annotation: options[UIApplication.OpenURLOptionsKey.annotation])
    }
    


}

