using LabBenchStudios.Pdt.Common;
using LabBenchStudios.Pdt.Data;

using UnityEngine;

public class TemperatureThresholdHandler: MonoBehaviour, IDataContextEventListener
{
    [SerializeField, Range(21.0f, 100.0f)]
    private float thresholdHigh = 25.0f;

    [SerializeField, Range(10.0f, 30.0f)]
    private float nominalMid = 20.0f;

    [SerializeField, Range(1.0f, 19.0f)]
    private float thresholdLow = 15.0f;

    private Renderer tempObjectRenderer = null;
    private Gradient tempGradient = null; 

     void Start()
    {
        // get renderer and create gradient
        this.tempObjectRenderer = gameObject.GetComponent<Renderer>();
        this.tempGradient = new Gradient();

        // use three gradients: red (highest val), green (mid val), blue (low val)
        GradientColorKey[] colorKey = new GradientColorKey[3];
        GradientAlphaKey[] alphaKey = new GradientAlphaKey[3];

        float high = 1.0f;
        float mid  = this.nominalMid / this.thresholdHigh;
        float low  = this.thresholdLow / this.thresholdHigh;

        if (mid >= 1.0f) mid = 0.5f;
        if (low >= 1.0f) low = 0.1f;

        //
        // provision color keys
        //

        // as value approaches thresholdHigh, color becomes more red
        colorKey[0].color = Color.red;
        colorKey[0].time  = high;

        // as value hovers at nominalMid, color is white
        colorKey[1].color = Color.white;
        colorKey[1].time = mid;

        // as value approaches thresholdLow, color becomes more blue
        colorKey[2].color = Color.blue;
        colorKey[2].time  = low;

        //
        // provision alpha keys
        //

        // as value moves from thresholdHigh to thresholdLow
        // alpha value renders color more translucent
        alphaKey[0].alpha = 0.85f;
        alphaKey[0].time  = high;

        alphaKey[1].alpha = 0.55f;
        alphaKey[1].time = mid;

        alphaKey[2].alpha = 0.25f;
        alphaKey[2].time  = low;

        this.tempGradient.SetKeys(colorKey, alphaKey);

        // set default color to configured mid-point
        Debug.Log("Nominal Mid Value: " + nominalMid);
        this.UpdateComponentColor(this.nominalMid);
    }

    // callback methods - only HandleSensorData() is used
    // others are required to implement the interface

    public void HandleActuatorData(ActuatorData data)
    {
        // ignore for now
    }

    public void HandleConnectionStateData(ConnectionStateData data)
    {
        // ignore for now
    }

    public void HandleMessageData(MessageData data)
    {
        // ignore for now
    }

    public void HandleSystemPerformanceData(SystemPerformanceData data)
    {
        // ignore for now
    }

    public void HandleSensorData(SensorData data)
    {
        if (data != null)
        {
            this.UpdateComponentColor(data.GetValue());
        }
    }

    private void UpdateComponentColor(float val)
    {
        if (this.tempObjectRenderer != null)
        {
            // scale value to something between 0.0f and 1.0f
            Debug.Log("Calling Update Component Color");
            float scaledVal = (val > 0.0f ? val / this.thresholdHigh : val);

            this.tempObjectRenderer.material.color = this.tempGradient.Evaluate(scaledVal);
        }
    }

}
