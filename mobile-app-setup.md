# 📱 LiveRoom AI - Mobile App Development Guide

## 🚀 Quick Setup Commands

### Create React Native Project
```bash
# Install React Native CLI
npm install -g react-native-cli

# Create new project
npx react-native init LiveRoomMobile
cd LiveRoomMobile

# Install essential dependencies
npm install @react-navigation/native @react-navigation/stack @react-navigation/bottom-tabs
npm install react-native-screens react-native-safe-area-context
npm install @react-native-async-storage/async-storage
npm install react-native-vector-icons
npm install react-native-linear-gradient
npm install react-native-gesture-handler
npm install react-native-reanimated
npm install axios
npm install react-native-paper
npm install react-native-elements
npm install react-native-gifted-chat

# For iOS
cd ios && pod install && cd ..

# For Android - add to android/app/build.gradle
# implementation 'androidx.appcompat:appcompat:1.1.0'
```

## 📁 Project Structure
```
LiveRoomMobile/
├── src/
│   ├── components/
│   │   ├── ChatBubble.tsx
│   │   ├── CharacterCard.tsx
│   │   └── LoadingSpinner.tsx
│   ├── screens/
│   │   ├── SplashScreen.tsx
│   │   ├── LoginScreen.tsx
│   │   ├── HomeScreen.tsx
│   │   ├── CharactersScreen.tsx
│   │   ├── ChatScreen.tsx
│   │   ├── ProfileScreen.tsx
│   │   └── SubscriptionScreen.tsx
│   ├── navigation/
│   │   ├── AppNavigator.tsx
│   │   └── AuthNavigator.tsx
│   ├── services/
│   │   ├── api.ts
│   │   ├── auth.ts
│   │   └── storage.ts
│   ├── utils/
│   │   ├── constants.ts
│   │   └── helpers.ts
│   └── types/
│       └── index.ts
├── android/
├── ios/
└── package.json
```

## 🎨 Key Components

### 1. Splash Screen
```typescript
// src/screens/SplashScreen.tsx
import React, { useEffect } from 'react';
import { View, Text, StyleSheet, Animated } from 'react-native';
import LinearGradient from 'react-native-linear-gradient';

const SplashScreen = ({ navigation }) => {
  const fadeAnim = new Animated.Value(0);

  useEffect(() => {
    Animated.timing(fadeAnim, {
      toValue: 1,
      duration: 2000,
      useNativeDriver: true,
    }).start();

    setTimeout(() => {
      navigation.replace('Auth');
    }, 3000);
  }, []);

  return (
    <LinearGradient
      colors={['#667eea', '#764ba2']}
      style={styles.container}
    >
      <Animated.View style={[styles.content, { opacity: fadeAnim }]}>
        <Text style={styles.title}>LiveRoom AI</Text>
        <Text style={styles.subtitle}>Your AI Companion Awaits</Text>
      </Animated.View>
    </LinearGradient>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  content: {
    alignItems: 'center',
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: 'white',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    color: 'rgba(255, 255, 255, 0.8)',
  },
});

export default SplashScreen;
```

### 2. Character Selection Screen
```typescript
// src/screens/CharactersScreen.tsx
import React, { useState, useEffect } from 'react';
import { View, FlatList, StyleSheet } from 'react-native';
import { CharacterCard } from '../components/CharacterCard';
import { apiService } from '../services/api';

const CharactersScreen = ({ navigation }) => {
  const [characters, setCharacters] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadCharacters();
  }, []);

  const loadCharacters = async () => {
    try {
      const response = await apiService.getCharacters();
      setCharacters(response.data);
    } catch (error) {
      console.error('Error loading characters:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCharacterSelect = (character) => {
    navigation.navigate('Chat', { character });
  };

  const renderCharacter = ({ item }) => (
    <CharacterCard
      character={item}
      onPress={() => handleCharacterSelect(item)}
    />
  );

  return (
    <View style={styles.container}>
      <FlatList
        data={characters}
        renderItem={renderCharacter}
        keyExtractor={(item) => item.id.toString()}
        numColumns={2}
        contentContainerStyle={styles.grid}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  grid: {
    padding: 16,
  },
});

export default CharactersScreen;
```

### 3. Chat Screen with Gifted Chat
```typescript
// src/screens/ChatScreen.tsx
import React, { useState, useEffect, useCallback } from 'react';
import { GiftedChat, IMessage } from 'react-native-gifted-chat';
import { apiService } from '../services/api';

const ChatScreen = ({ route }) => {
  const { character } = route.params;
  const [messages, setMessages] = useState<IMessage[]>([]);
  const [isTyping, setIsTyping] = useState(false);

  useEffect(() => {
    setMessages([
      {
        _id: 1,
        text: `Hey there! I'm ${character.name} 💕 I'm so excited to chat with you!`,
        createdAt: new Date(),
        user: {
          _id: 2,
          name: character.name,
          avatar: character.image,
        },
      },
    ]);
  }, []);

  const onSend = useCallback(async (newMessages = []) => {
    setMessages(previousMessages =>
      GiftedChat.append(previousMessages, newMessages)
    );

    setIsTyping(true);
    
    try {
      const response = await apiService.sendMessage({
        message: newMessages[0].text,
        character_id: character.id,
        user_id: 1,
      });

      const aiMessage: IMessage = {
        _id: Math.round(Math.random() * 1000000),
        text: response.data.response,
        createdAt: new Date(),
        user: {
          _id: 2,
          name: character.name,
          avatar: character.image,
        },
      };

      setMessages(previousMessages =>
        GiftedChat.append(previousMessages, [aiMessage])
      );
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setIsTyping(false);
    }
  }, [character]);

  return (
    <GiftedChat
      messages={messages}
      onSend={onSend}
      user={{
        _id: 1,
      }}
      isTyping={isTyping}
      placeholder="Type a message..."
      alwaysShowSend
      scrollToBottom
    />
  );
};

export default ChatScreen;
```

## 🔧 API Service Setup

```typescript
// src/services/api.ts
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_BASE_URL = 'https://your-railway-backend.railway.app/api/v1';

class ApiService {
  private api;

  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
    });

    // Add auth token to requests
    this.api.interceptors.request.use(async (config) => {
      const token = await AsyncStorage.getItem('authToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  async getCharacters() {
    return this.api.get('/characters/');
  }

  async sendMessage(data: { message: string; character_id: number; user_id: number }) {
    return this.api.post('/chat/send', data);
  }

  async createPaymentOrder(planId: string) {
    return this.api.post('/payments/create-order', { plan: planId });
  }

  async getSubscriptionStatus() {
    return this.api.get('/subscriptions/status');
  }
}

export const apiService = new ApiService();
```

## 📱 In-App Purchases Setup

### Android (Google Play Billing)
```bash
npm install react-native-iap
```

```typescript
// src/services/purchases.ts
import RNIap, {
  Product,
  ProductPurchase,
  SubscriptionPurchase,
  PurchaseError,
} from 'react-native-iap';

const itemSkus = Platform.select({
  ios: ['com.liveroom.basic', 'com.liveroom.pro'],
  android: ['basic_plan', 'pro_plan'],
});

class PurchaseService {
  async initConnection() {
    try {
      await RNIap.initConnection();
      console.log('IAP connection initialized');
    } catch (error) {
      console.error('Error initializing IAP:', error);
    }
  }

  async getProducts() {
    try {
      const products = await RNIap.getSubscriptions(itemSkus);
      return products;
    } catch (error) {
      console.error('Error getting products:', error);
      return [];
    }
  }

  async purchaseSubscription(sku: string) {
    try {
      const purchase = await RNIap.requestSubscription(sku);
      return purchase;
    } catch (error) {
      console.error('Purchase error:', error);
      throw error;
    }
  }
}

export const purchaseService = new PurchaseService();
```

## 🎨 UI Components

### Character Card Component
```typescript
// src/components/CharacterCard.tsx
import React from 'react';
import { View, Text, Image, TouchableOpacity, StyleSheet } from 'react-native';
import LinearGradient from 'react-native-linear-gradient';

interface CharacterCardProps {
  character: {
    id: number;
    name: string;
    image: string;
    description: string;
  };
  onPress: () => void;
}

const CharacterCard: React.FC<CharacterCardProps> = ({ character, onPress }) => {
  return (
    <TouchableOpacity style={styles.container} onPress={onPress}>
      <LinearGradient
        colors={['rgba(255, 255, 255, 0.1)', 'rgba(255, 255, 255, 0.05)']}
        style={styles.card}
      >
        <Image source={{ uri: character.image }} style={styles.image} />
        <Text style={styles.name}>{character.name}</Text>
        <Text style={styles.description} numberOfLines={2}>
          {character.description}
        </Text>
      </LinearGradient>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    margin: 8,
  },
  card: {
    borderRadius: 16,
    padding: 16,
    alignItems: 'center',
    minHeight: 200,
  },
  image: {
    width: 80,
    height: 80,
    borderRadius: 40,
    marginBottom: 12,
  },
  name: {
    fontSize: 16,
    fontWeight: 'bold',
    color: 'white',
    textAlign: 'center',
    marginBottom: 8,
  },
  description: {
    fontSize: 12,
    color: 'rgba(255, 255, 255, 0.8)',
    textAlign: 'center',
    lineHeight: 16,
  },
});

export default CharacterCard;
```

## 🚀 Build & Deploy

### Android Build
```bash
# Generate signed APK
cd android
./gradlew assembleRelease

# Generate AAB for Play Store
./gradlew bundleRelease
```

### iOS Build
```bash
# Open in Xcode
open ios/LiveRoomMobile.xcworkspace

# Archive and upload to App Store Connect
```

## 📊 Analytics Integration

```bash
npm install @react-native-firebase/app @react-native-firebase/analytics
```

```typescript
// src/services/analytics.ts
import analytics from '@react-native-firebase/analytics';

class AnalyticsService {
  async logEvent(eventName: string, parameters?: object) {
    await analytics().logEvent(eventName, parameters);
  }

  async logScreenView(screenName: string) {
    await analytics().logScreenView({
      screen_name: screenName,
      screen_class: screenName,
    });
  }

  async setUserId(userId: string) {
    await analytics().setUserId(userId);
  }
}

export const analyticsService = new AnalyticsService();
```

## 🔔 Push Notifications

```bash
npm install @react-native-firebase/messaging
```

```typescript
// src/services/notifications.ts
import messaging from '@react-native-firebase/messaging';

class NotificationService {
  async requestPermission() {
    const authStatus = await messaging().requestPermission();
    return authStatus === messaging.AuthorizationStatus.AUTHORIZED ||
           authStatus === messaging.AuthorizationStatus.PROVISIONAL;
  }

  async getToken() {
    return await messaging().getToken();
  }

  setupMessageHandlers() {
    messaging().onMessage(async remoteMessage => {
      console.log('Foreground message:', remoteMessage);
    });

    messaging().setBackgroundMessageHandler(async remoteMessage => {
      console.log('Background message:', remoteMessage);
    });
  }
}

export const notificationService = new NotificationService();
```

## 🎯 Next Steps

1. **Setup Development Environment**: Install React Native CLI and dependencies
2. **Create Project**: Use the commands above to create the mobile app
3. **Implement Core Features**: Start with splash screen and character selection
4. **Add Chat Functionality**: Integrate with your backend API
5. **Setup In-App Purchases**: Configure Google Play and App Store billing
6. **Add Analytics**: Track user behavior and engagement
7. **Test Thoroughly**: Test on multiple devices and OS versions
8. **Deploy to Stores**: Submit to Google Play Store and Apple App Store

The mobile app will significantly increase user engagement and provide additional revenue through in-app purchases and subscriptions!
