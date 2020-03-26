using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DoThings : MonoBehaviour
{
    Vector3 currentScale = Vector3.one;
    Vector3 goalScale = new Vector3();
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        currentScale = Vector3.Lerp(currentScale, goalScale, 0.1f);
        transform.localScale = currentScale;
    }
    public void UpdateValue(PollutionData pd) {
        Vector3 s = new Vector3(pd.pm10, pd.pm25, pd.co2);
        s=Vector3.one+s*2;
        goalScale = s;
    }
}
