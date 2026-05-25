<script setup>
defineProps({
  titlePrimary: { type: String, default: 'Talent' },
  titleSecondary: { type: String, default: 'Finder' },
  subtitle: { type: String, default: 'Smarter hiring starts here' },
});
</script>

<template>
  <div class="min-vh-100 d-flex justify-content-center align-items-center">
    <div class="card mb-3 shadow-sm overflow-hidden" style="max-width: 900px; border: none">
      <div class="row g-0">
        <div class="col-md-6 bg-light">
          <div class="text-center h-100 d-flex flex-column justify-content-between">
            <div class="pt-5">
              <h1 class="card-title fw-bolder display-5 m-0">
                <span class="text-primary">{{ titlePrimary }}</span> {{ titleSecondary }}
              </h1>
              <p class="lead text-muted">{{ subtitle }}</p>
            </div>

            <div class="mt-auto d-none d-md-block">
              <img
                src="@/assets/images/abstract-waves.png"
                class="img-fluid"
                alt=""
                style="margin-bottom: -1px"
              />
            </div>
          </div>
        </div>

        <div class="col-md-6 d-flex align-items-center bg-light">
          <div class="card-body p-4 p-lg-5 w-100">
            <slot></slot>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
