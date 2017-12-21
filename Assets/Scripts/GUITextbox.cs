using System.Collections;
using UnityEngine.UI;
using UnityEngine;


public class GUITextbox : MonoBehaviour {
    bool triggered;
    public void OnTriggerEnter(Collider other)
    {
        triggered = true;
    }
    void OnGui()
    {
        if (triggered)
        {
            Debug.Log("Text box displayed.");
            GUI.Box(new Rect(300, 300, 500, 200), "Hello World!");
        }
    }
    public void OnTriggerExit(Collider other)
    {
        //exit dialog
    }
}

