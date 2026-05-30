<script setup lang="ts">
import { ref } from "vue";

const username = ref("");
const password = ref("");
const token = ref(localStorage.getItem("access_token"));
const error = ref("");

const login = async () => {
  error.value = "";

  const response = await fetch(
    "http://127.0.0.1:8000/auth/login",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value,
      }),
    }
  );

  if (!response.ok) {
    error.value = "Usuario o contraseña incorrectos";
    return;
  }

  const data = await response.json();

  localStorage.setItem(
    "access_token",
    data.access_token
  );

  token.value = data.access_token;
};

const logout = () => {
  localStorage.removeItem("access_token");
  token.value = null;
};

const searchItems = async () => {
  const response = await fetch(
    "http://127.0.0.1:8000/items/search",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token.value}`,
      },
      body: JSON.stringify({}),
    }
  );

  if (response.status === 401) {
    logout();
    return;
  }

  const data = await response.json();
  items.value = data;
  console.log(data);
};

const items = ref([]);


</script>


<template>
  <div v-if="!token">
    <h1>Login</h1>

    <input
      v-model="username"
      placeholder="Usuario"
    />

    <input
      v-model="password"
      type="password"
      placeholder="Contraseña"
    />

    <button @click="login">
      Login
    </button>
    <p v-if="error">
       {{ error }}
    </p>
  </div>

  <div v-else>
    <h1>Área protegida</h1>
    <button @click="logout">
    Logout
    </button>
    <button @click="searchItems">
      Buscar Artículos
    </button>
    <ul>
      <li v-for="item in items" :key="item.id">
        {{ item.sku }}
      </li>
    </ul>
  </div>
</template>