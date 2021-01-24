const PoweredUP = require("node-poweredup");
const poweredUP = new PoweredUP.PoweredUP();
const mqtt = require("mqtt")
const client = mqtt.connect("mqtt://localhost")
let frontMotor = {}
let rearMotor = {}
let steerMotor = {}
let ready = false
let lastSteeringPower = 0
let lastMotorPower = 0

// Subscribe motor commands
client.subscribe("control/motor/power")
client.subscribe("control/steering/power")

poweredUP.on("discover", async (hub) => { // Wait to discover a Hub
    console.log(`Discovered ${hub.name}!`)
    await hub.connect() // Connect to the Hub
    frontMotor = await hub.waitForDeviceAtPort("A") // Motor controlling front wheels on port A
    rearMotor  = await hub.waitForDeviceAtPort("B") // Motor controlling rear wheels on port B
    steerMotor = await hub.waitForDeviceAtPort("C") // Motor controlling steering on port C
    console.log("Connected")

    console.log("Hub name        : " + hub.name)
    console.log("FW version      : " + hub.firmwareVersion)
    console.log("HW version      : " + hub.hardwareVersion)
    console.log("Battery level   : " + hub.batteryLevel)
    console.log("Front motor type: " + frontMotor.typeName)
    console.log("Rear motor type : " + rearMotor.typeName)
    console.log("Steer motor type: " + steerMotor.typeName)
    console.log("Steering angle: " + steerMotor.angle)

    client.publish("hub/status", "Connected")
    client.publish("hub/fw", hub.firmwareVersion)
    client.publish("hub/hw", hub.hardwareVersion)
    client.publish("hub/battery", hub.batteryLevel.toString())

    await steerMotor.gotoRealZero(100)
    await hub.sleep(500)

    console.log("Steering right...")
    //await steerMotor.gotoAngle(90, 100)
    steerMotor.setPower(50)
    await hub.sleep(500)

    console.log("Going to zero...")
    await steerMotor.gotoRealZero(100)
    await hub.sleep(500)

    console.log("Steering left...")
    //await steerMotor.gotoAngle(-90, 100)
    steerMotor.setPower(-50)
    await hub.sleep(500)

    console.log("Going to zero...")
    await steerMotor.gotoRealZero(100)

    ready = true

    //console.log("Ramping motors to -10% then brake")
    /*frontMotor.rampPower(-10)
    rearMotor.rampPower(-10)
    setTimeout(() => {
        console.log("Ramping motors to -10% then brake")
        frontMotor.brake()
        rearMotor.brake()
    }, 1000)


    //console.log("Ramping motors to 10% then brake")
    frontMotor.rampPower(10)
    rearMotor.rampPower(10)

    setTimeout(() => {
        console.log('Ramping motors to 10% then brake')
        frontMotor.brake()
        rearMotor.brake()
    }, 1000)*/

    console.log("Initialization sequence done!")



    //console.log("Disconnecting...")
    //await hub.disconnect()


    /*while (true) { // Repeat indefinitely
        console.log("Running motor B at speed 50");
        motorB.setPower(50); // Start a motor attached to port B to run a 3/4 speed (75) indefinitely
        console.log("Running motor A at speed 100 for 2 seconds");
        motorA.setPower(100); // Run a motor attached to port A for 2 seconds at maximum speed (100) then stop
        await hub.sleep(2000);
        motorA.brake();
        await hub.sleep(1000); // Do nothing for 1 second
        console.log("Running motor A at speed -30 for 1 second");
        motorA.setPower(-30); // Run a motor attached to port A for 2 seconds at 1/2 speed in reverse (-50) then stop
        await hub.sleep(2000);
        motorA.brake();
        await hub.sleep(1000); // Do nothing for 1 second
    }*/

});

client.on('message', async(topic, message) => {
    if(ready) {
        power = 0
        if (topic === 'control/motor/power') {
            power = -1 * parseInt(message.toString(), 10) // Moving forward negative, backward positive

            if(lastMotorPower !== power) {
                //console.log('Setting motors power to ' + message)
                frontMotor.setPower(power)
                rearMotor.setPower(power)
                steerMotor.setPower(lastSteeringPower)
                lastMotorPower = power
            }
        }
        else if (topic === 'control/steering/power') {
            power = parseInt(message.toString(), 10)

            //console.log('Setting steering power to ' + power + ' Last: ' + lastSteeringPower)

            if(lastSteeringPower !== power) {
                if (power !== 0) {
                    //console.log('Steering...')
                    steerMotor.setPower(parseInt(message.toString(), 10))
                } else {
                    //console.log('Going to real zero....')
                    //await steerMotor.gotoRealZero(10)
                    await steerMotor.gotoAngle(0)
                    steerMotor.setPower(0)
                }
                lastSteeringPower = power
            }
        }
        else {
            console.log('Unknown control command')
        }
    }
    else {
        console.log('Control command received but not connected to any hub!')
    }
})

poweredUP.scan(); // Start scanning for Hubs
console.log("Scanning for Hubs...");