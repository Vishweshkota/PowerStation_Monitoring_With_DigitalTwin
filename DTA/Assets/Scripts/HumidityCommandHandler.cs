using LabBenchStudios.Pdt.Common;
using LabBenchStudios.Pdt.Data;
using LabBenchStudios.Pdt.Plexus;

using UnityEngine;

public class HumidityCommandHandler: MonoBehaviour, IDataContextExtendedListener
{
    [SerializeField]
    private bool enableThresholdCrossingActuation = true;

    [SerializeField, Range(60.0f, 100.0f)]
    private float thresholdHigh = 80.0f;

    [SerializeField, Range(1.0f, 30.0f)]
    private float thresholdLow = 10.0f;

    [SerializeField, Range(1.0f, 100.0f)]
    private float adjustmentPercentage = 10.0f;

    [SerializeField, Range(1, 100)]
    private int maxPermittedThresholdCrossings = 2;

    [SerializeField, Range(1, 100)]
    private int nominalReadingsToReset = 10;

    private int highThresholdCrossingCount = 0;
    private int lowThresholdCrossingCount = 0;
    private int nominalReadingsCount = 0;

    private IDigitalTwinStateProcessor dtStateProcessor = null;
    private ThresholdCrossingContainer thresholdCrossingContainer = null;

    void Start()
    {
        this.thresholdCrossingContainer = new ThresholdCrossingContainer();
    }

    // public methods

    public ThresholdCrossingContainer GetThresholdCrossingContainer()
    {
        Debug.Log("Threshold Crossing Container" + this.thresholdCrossingContainer);
        return this.thresholdCrossingContainer;
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
        // allow controller to enable / disable auto-threshold crossing actuation
        if (data != null && this.enableThresholdCrossingActuation)
        {
            float val = data.GetValue();
            float changeFactor = this.adjustmentPercentage / 100.0f;

            if (val > this.thresholdHigh)
            {
                // a simple crossing check: increment threshold crossing count immediately;
                // if it exceeds thresholdcrossings to actuate, generate the actuation event
                if (++this.highThresholdCrossingCount > this.maxPermittedThresholdCrossings)
                {
                    // abs value ensures we're always subtracting a positive value
                    // from the actual, whether actual is positive or negative
                    float changeVal = Mathf.Abs(changeFactor * this.thresholdHigh);
                    float adjustedVal = val - changeVal;

                    // generate and send actuation event, and reset high threshold crossings
                    this.GenerateAndSendActuationEvent(adjustedVal);

                    this.highThresholdCrossingCount = 0;
                }
            }
            else if (val < this.thresholdLow)
            {
                // a simple crossing check: increment threshold crossing count immediately;
                // if it exceeds thresholdcrossings to actuate, generate the actuation event
                if (++this.lowThresholdCrossingCount > this.maxPermittedThresholdCrossings)
                {
                    // abs value ensures we're always adding a positive value
                    // to the actual, whether actual is positive or negative
                    float changeVal = Mathf.Abs(changeFactor * this.thresholdLow);
                    float adjustedVal = val + changeVal;

                    // generate and send actuation event, and reset low threshold crossings
                    this.GenerateAndSendActuationEvent(adjustedVal);

                    this.lowThresholdCrossingCount = 0;
                }
            }
            else
            {
                if (this.nominalReadingsCount++ >= this.nominalReadingsToReset)
                {
                    this.highThresholdCrossingCount = 0;
                    this.lowThresholdCrossingCount = 0;
                }
            }
        }
    }

    public void SetDigitalTwinStateProcessor(IDigitalTwinStateProcessor dtStateProcessor)
    {
        if (dtStateProcessor != null)
        {
            this.dtStateProcessor = dtStateProcessor;
        }
    }

    // private methods

    private void GenerateAndSendActuationEvent(float adjustedVal)
    {
        if (this.dtStateProcessor != null)
        {
            ActuatorData data = new();

            // note: recipient should be able to auto shut-off
            // hvac once desired temp is reached - it should not
            // have to rely on a follow up command from a remote
            // system (hosted within the DTA)
            data.SetName(ConfigConst.ACTUATOR_CMD);
            data.SetDeviceID(this.dtStateProcessor.GetDeviceID());
            data.SetTypeCategoryID(ConfigConst.ENV_TYPE_CATEGORY);
            data.SetTypeID(ConfigConst.HUMIDIFIER_ACTUATOR_TYPE);
            data.SetCommand(ConfigConst.COMMAND_ON);
            data.SetValue(adjustedVal);
            data.SetStateData("humidifier");
            data.SetLocationID("edgedevice001");

            // state processor will ensure the target device is set
            ResourceNameContainer resource = this.dtStateProcessor.GenerateOutgoingStateUpdate(data);
            
            EventProcessor.GetInstance().ProcessStateUpdateToPhysicalThing(resource);
            Debug.Log("Debug_Event Processor" + EventProcessor.GetInstance().ProcessStateUpdateToPhysicalThing(resource));
        }
        else
        {
            Debug.LogError("No Digital Twin State Processor set. Ignoring actuation event.");
        }
    }
}
