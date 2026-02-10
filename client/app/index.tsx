import { createNativeStackNavigator } from "@react-navigation/native-stack";
import React from "react";
import Home from "../components/Home";
import Login from "../components/login";
import useWebSocket from "../hook/useWebSocket";

// Create a Stack Navigator
const Stack = createNativeStackNavigator();

export default function Index() {
  // Create ONE WebSocket for the whole app
  const webSocket = useWebSocket("10.0.2.2", 3000);

  return (
    <Stack.Navigator
      initialRouteName="Login" // start with Login
      screenOptions={{
        headerShown: false, // hide headers, optional
      }}
    >
      <Stack.Screen name="Login">
        {(props) => <Login {...props} webSocket={webSocket} />}
      </Stack.Screen>
      <Stack.Screen name="Home" component={Home} />
    </Stack.Navigator>
  );
}
