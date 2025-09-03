// In App.js in a new project

import * as React from "react";
import { View, Text } from "react-native";
import { createStaticNavigation } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";

function HomeScreen() {
  return (
    <View style={{ flex: 1, alignItems: "center", justifyContent: "center" }}>
      <Text style={{  }}>Hello World!</Text>
    </View>
  );
}

const RootStack = createNativeStackNavigator({
  initialRouteName: "Home",
  screenOptions: {
    headerStyle: { backgroundColor: "blue" },
    title: "Hello World",
    headerTitleStyle: {
      fontWeight: "bold",
      color: "white"
    },
  },
  screens: {
    Home: HomeScreen,
  },
});

const Navigation = createStaticNavigation(RootStack);

export default function App() {
  return <Navigation />;
}
