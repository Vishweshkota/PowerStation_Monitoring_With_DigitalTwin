using LabBenchStudios.Pdt.Common;
using LabBenchStudios.Pdt.Data;

using UnityEngine;

public class PowerGenerationThresholdAnimationHandler : MonoBehaviour, IDataContextEventListener
{
    [SerializeField, Range(50001.0f, 100000.0f)]
    private float thresholdHigh = 60000.0f;

    [SerializeField, Range(35001.0f, 50000.0f)]
    private float nominalMidHigh = 40000.0f;

    [SerializeField, Range(15001.0f, 35000.0f)]
    private float nominalMidLow = 20000.0f;

    [SerializeField, Range(1.0f, 15000.0f)]
    private float thresholdLow = 10000.0f;

    private Renderer batteryStorageObjectRenderer = null;
    private Gradient batteryStorageGradient = null;

    void Start()
    {
        // get renderer and create gradient
        this.batteryStorageObjectRenderer = gameObject.GetComponent<Renderer>();
        this.batteryStorageGradient = new Gradient();

        // use three gradients: red (highest val), green (mid val), blue (low val)
        GradientColorKey[] colorKey = new GradientColorKey[4];
        GradientAlphaKey[] alphaKey = new GradientAlphaKey[4];

        float high = 1.0f;
        float midHigh = this.nominalMidHigh / this.thresholdHigh;
        float midLow = this.nominalMidLow / this.thresholdHigh;
        float low  = this.thresholdLow / this.thresholdHigh;

        if (midHigh >= 1.0f) midHigh = 0.6f;
        if (midLow >= 1.0f) midLow = 0.3f;
        if (low >= 1.0f) low = 0.1f;

        //
        // provision color keys
        //

        // as curValue approaches thresholdHigh, color becomes more green
        colorKey[0].color = Color.green;
        colorKey[0].time  = high;

        // as curValue hovers at midHigh, color is blue
        colorKey[1].color = Color.blue;
        colorKey[1].time = midHigh;

        // as curValue hovers at midLow, color is yellow
        colorKey[2].color = Color.yellow;
        colorKey[2].time = midLow;

        // as curValue approaches thresholdLow, color becomes more red
        colorKey[3].color = Color.red;
        colorKey[3].time  = low;

        //
        // provision alpha keys
        //

        // as curValue moves from thresholdHigh to thresholdLow
        // alpha curValue renders color more translucent
        alphaKey[0].alpha = 0.85f;
        alphaKey[0].time  = high;
        alphaKey[1].alpha = 0.65f;
        alphaKey[1].time = midHigh;
        alphaKey[2].alpha = 0.45f;
        alphaKey[2].time = midLow;
        alphaKey[3].alpha = 0.25f;
        alphaKey[3].time  = low;

        this.batteryStorageGradient.SetKeys(colorKey, alphaKey);

        // set default color to configured mid-point
        this.UpdateComponentColor(this.nominalMidLow);
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
            if (data.GetTypeID() == ConfigConst.WIND_TURBINE_POWER_OUTPUT_SENSOR_TYPE)
            {
                this.UpdateComponentColor(data.GetValue());
            }
        }
    }

    private void UpdateComponentColor(float val)
    {
        if (this.batteryStorageObjectRenderer != null)
        {
            // scale curValue to something between 0.0f and 1.0f
            float scaledVal = (val > 0.0f ? val / this.thresholdHigh : val);

            this.batteryStorageObjectRenderer.material.color = this.batteryStorageGradient.Evaluate(scaledVal);
        }
    }
}