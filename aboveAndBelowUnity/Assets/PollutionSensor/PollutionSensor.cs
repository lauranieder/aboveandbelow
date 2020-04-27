using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using SimpleJSON;


[RequireComponent(typeof(PollutionLogin))]
public class PollutionSensor : MonoBehaviour
{
    // A SAVOIR
    // COMBIEN DE DATA DIFFERENTES (pollution level, localisation, autre ?)
    // QUELLE QUANTITE EN MEME TEMPS
    //
    private string urlBase = "https://io.adafruit.com/api/v2/";
    private string urlGroup = "/groups/";
    private string urlFeeds = "/feeds/";
    private string urlKey = "?x-aio-key=";
    // private string args = "&limit=";
    //
    [Header("Feed to read on adafruit-io, each Pollution Sensor will have it's own feed")]
    public string feed = "test";
    //
    [Header("Automatically generated - here for debug - you can copy paste in browser to check raw json results")]
    public string finalUrl;
    //
    [Header("Check adafruitIO limitations")]
    public float timingUpdate = 2;
    //
    [Header("If you want GameObjects 'UpdateValue()' function to be called")]
    public GameObject[] toNotify;
    //
    [Header("Last data received - this data object will be send to the gamobject 'toNotify'")]
    public PollutionData newData;
    private string oldRawData;
    //
    public bool fakeIt = false;
    //
    void Start() {
        StartCoroutine("PerformCheck");
    }
    // Update is called once per frame
    void Update() {
        if(fakeIt == true) {
            FakeData();
            fakeIt = false;
        }
    }
    IEnumerator PerformCheck() {
        while(true) {
            finalUrl = urlBase+PollutionLogin._username+urlFeeds+feed+"/data/last"+urlKey+PollutionLogin._apiKey;
            //
            WWWForm form = new WWWForm();
            //form.AddField("myField", "myData");
            //
            using (UnityWebRequest www = UnityWebRequest.Get(finalUrl)) {
                yield return www.SendWebRequest();
                //
                if (www.isNetworkError || www.isHttpError) {
                    Debug.Log(www.error);
                } else {
                    //Debug.Log("Form upload complete!");
                    //Debug.Log(www.downloadHandler.text);
                    // JSONObject = JSON.Parse(jsonString);
                    newData = new PollutionData(www.downloadHandler.text);
                    if(oldRawData == null || !www.downloadHandler.text.Equals(oldRawData)) {
                        oldRawData = www.downloadHandler.text;
                        Debug.Log("Updated data");
                        Dispatch(newData);
                    } else {
                        // If it's the same
                        Debug.Log("No update (same data)");
                    }
                }
            }
            yield return new WaitForSeconds(timingUpdate);
        }
    }
    void FakeData() {
        Debug.Log("FakeIt");
        newData = new PollutionData();
        newData.Randomize();
        Dispatch(newData);
    }
    void Dispatch(PollutionData newData) {
        foreach(GameObject go in toNotify) {
            go.SendMessage("UpdateValue", newData);
        }
    }
}
[System.Serializable]
public class PollutionData {
    public System.DateTime updated;

    public System.DateTime updatedGPS;
    //
    public float lat; // -90 to 90 deg
    public float lon; // -180 to 180 deg

    // Meters or Feets
    public float altitudeM; // 0 to 8848
    public float altitudeF; // 0 to 29028
    // Fahrenheit or Celcius
    public float tempF; // 0 to 212 degF
    public float tempC; // 0 to 100 degC
    // Pascal and InHg???
    public float pressurePa;
    public float pressureInHg;
    // Humidity
    public float humidityRH; // 0% to 100%
    // TVOC
    public float tvoc;
    // Co2
    public float co2;
    // PM 2.5
    public float pm25;
    // PM 10
    public float pm10;
    // NOT available
    // public float no2;
    // public float psi;
    //
    public string raw = "";
    //
    public PollutionData(string data) {
        raw = data;
        JSONNode json = SimpleJSON.JSON.Parse(data);

        updated = System.DateTime.Parse(json["updated_at"]);

        string value = json["value"];
        //
        JSONNode jsonValue = SimpleJSON.JSON.Parse(value);
        //
        altitudeM = jsonValue["altitudeM"];
        altitudeF = jsonValue["altitudeF"];
        //
        tempF = jsonValue["tempF"];
        tempC = jsonValue["tempC"];
        //
        humidityRH= jsonValue["humidityRH"];
        //
        pressurePa = jsonValue["pressurePa"];
        pressureInHg = jsonValue["pressureInHg"];
        //
        pm25 = jsonValue["pm25"];
        pm10 = jsonValue["pm10"];
        co2 = jsonValue["co2"];
        tvoc = jsonValue["tvoc"];

        lat = jsonValue["lat"];
        lon = jsonValue["lon"];
        updatedGPS = System.DateTime.Parse(jsonValue["gdat"]);
    }
    public void Randomize() {
        lat = Random.Range(-90f, 90f);
        lon = Random.Range(-180f, 180f);
        altitudeM = Random.Range(0f, 8848f);
        altitudeF = Random.Range(0f, 29028f);
        tempF = Random.Range(0f, 212f);
        tempC = Random.Range(0f, 100f);
        humidityRH = Random.Range(0f, 100f);
        //
        pressurePa = Random.Range(0f, 1f);
        pressureInHg = Random.Range(0f, 1f);
        pm25 = Random.Range(0f, 1f);
        pm10 = Random.Range(0f, 1f);
        co2 = Random.Range(0f, 1f);
        tvoc = Random.Range(0f, 1f);
        updated = System.DateTime.Now;
        updatedGPS = System.DateTime.Now;
    }
    public PollutionData() {
    }
}
