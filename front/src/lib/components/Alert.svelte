<script lang="ts">
  let {
    value = $bindable(),
    type,
    message = "",
    isOpen = false,
    duration = 3000,
  } = $props();

  let interval: number;

  export function show(msg: string = message, type: string = "success") {
    type = type;
    message = msg;
    isOpen = true;

    const progressBar = document.querySelector(
      ".alert__progress"
    ) as HTMLDivElement;

    if (duration > 0) {
      progressBar.style.width = "100%";
      let widthPercentage = 100;

      interval = setInterval(() => {
        if (progressBar.offsetWidth > 0) {
          progressBar.style.width = `${widthPercentage--}%`;
        } else hide()
      }, duration / 100);
    }
  }

  export function hide() {
    clearInterval(interval);
    isOpen = false;
  }
</script>

<div bind:this={value} class="alert df {type}" class:open={isOpen}>
  {message}
  <button class="df" aria-label="close" onclick={hide}>
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="15"
      height="15"
      viewBox="0 0 30 30"
      fill="none"
    >
      <path
        d="M15 18.1939L3.82129 29.3726C3.40304 29.7909 2.87072 30 2.22433 30C1.57795 30 1.04563 29.7909 0.627376 29.3726C0.209125 28.9544 0 28.4221 0 27.7757C0 27.1293 0.209125 26.597 0.627376 26.1787L11.8061 15L0.627376 3.82129C0.209125 3.40304 0 2.87072 0 2.22433C0 1.57795 0.209125 1.04563 0.627376 0.627376C1.04563 0.209125 1.57795 0 2.22433 0C2.87072 0 3.40304 0.209125 3.82129 0.627376L15 11.8061L26.1787 0.627376C26.597 0.209125 27.1293 0 27.7757 0C28.4221 0 28.9544 0.209125 29.3726 0.627376C29.7909 1.04563 30 1.57795 30 2.22433C30 2.87072 29.7909 3.40304 29.3726 3.82129L18.1939 15L29.3726 26.1787C29.7909 26.597 30 27.1293 30 27.7757C30 28.4221 29.7909 28.9544 29.3726 29.3726C28.9544 29.7909 28.4221 30 27.7757 30C27.1293 30 26.597 29.7909 26.1787 29.3726L15 18.1939Z"
        fill="#e90017"
      />
    </svg>
  </button>
  <div class="alert__progress"></div>
</div>

<style lang="scss">
  .alert {
    gap: 10px;
    width: auto;
    left: 50%;
    top: 10px;
    opacity: 0;
    transform: translateX(-50%) translateY(-150%);
    position: absolute;
    padding: 10px;
    border-radius: 5px;
    overflow: hidden;
    margin-bottom: 10px;
    color: white;
    text-align: center;
    transition: all 200ms ease-out;

    &__progress {
      height: 3px;
      width: 0;
      position: absolute;
      bottom: 0;
      left: 0;
      background-color: #e90017;
    }

    &.open {
      transform: translateX(-50%) translateY(0);
      opacity: 1;
    }

    &.success {
      background-color: #00ac28;
      color: #00ff3c;
    }

    &.error {
      background-color: #6b0009;
      color: #e90017;
    }

    &.warning {
      background-color: #f7b733;
      color: #ffde59;
    }
  }

  button {
    background-color: transparent;
  }
</style>
