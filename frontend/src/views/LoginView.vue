<script setup>
import { ref } from 'vue';

const email = ref('');
const password = ref('');

async function login() {
  console.log('Logging in with:', email.value);
}
</script>

<template>
  <div class="min-vh-100 d-flex justify-content-center align-items-center">
    <div class="card mb-3 overflow-hidden" style="max-width: 900px">
      <div class="row g-0">
        <div class="col-md-6 bg-white">
          <div class="text-center">
            <h1 class="card-title fw-bolder display-5 pt-5 m-0">
              <span class="text-primary">Talent</span> Finder
            </h1>
            <p class="lead text-muted">Smarter hiring starts here</p>

            <div class="mt-4 d-none d-md-block">
              <img
                src="@/assets/images/abstract-waves.png"
                class="img-fluid rounded"
                alt="Wave Image"
              />
            </div>
          </div>
        </div>

        <div class="col-md-6 d-flex align-items-center">
          <div class="card-body p-4 p-lg-5">
            <h4 class="text-secondary mb-4">Welcome Back</h4>

            <form @submit.prevent="login">
              <div class="mb-3">
                <label for="email" class="form-label small fw-bold">Email address</label>
                <div class="input-group">
                  <span class="input-group-text bg-light border-end-0">
                    <i class="bi bi-envelope text-muted"></i>
                  </span>
                  <input
                    type="email"
                    class="form-control border-start-0"
                    v-model="email"
                    id="email"
                    placeholder="your@account.com"
                    required
                    autofocus
                  />
                </div>
              </div>

              <div class="mb-4">
                <label for="password" class="form-label small fw-bold">Password</label>
                <div class="input-group">
                  <span class="input-group-text bg-light border-end-0">
                    <i class="bi bi-lock text-muted"></i>
                  </span>
                  <input
                    type="password"
                    v-model="password"
                    class="form-control border-start-0"
                    id="password"
                    placeholder="········"
                    required
                  />
                </div>
              </div>

              <!-- Botón de Acción -->
              <div class="d-grid">
                <button type="submit" class="btn btn-primary btn-lg">Sign In</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
