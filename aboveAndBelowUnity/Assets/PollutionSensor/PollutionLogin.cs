using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using SimpleJSON;

public class PollutionLogin : MonoBehaviour
{
    public static string _username;
    public static string _apiKey;
    //
    [Header("You can have multiple Pollution Sensor. You need at least one Pollution Login (added automatically)")]
    public string username;
    public string apiKey;
    //
    void Awake() {
        _username = username;
        _apiKey = apiKey;
    }
    void Start() {
    }
    // Update is called once per frame
    void Update() {
    }
}