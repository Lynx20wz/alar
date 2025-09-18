<script lang="ts">
  let { value = $bindable(), type, message, isOpen = false, duration = 3000} = $props();

  export function show(msg: string, type: string = 'success') {
    message = msg;
    type = type;
    isOpen = true;
    
    setTimeout(() => {
      isOpen = false;
    }, duration);
  }

  export function hide() {
    isOpen = false;
  };

  $inspect(isOpen)
</script>

<div bind:this={value} class="alert df {type}" class:open={isOpen}>
  {message}
  <button on:click={hide}>Close</button>
</div>

<style lang="scss">
.alert {
  display: none;
  gap: 5px;
  top: 5px;
  width: 100px;
  left: 50%;
  transform: translateX(-50%);
  position: absolute;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 10px;
  color: white;
  text-align: center;
  transition: opacity 300ms ease;

  &.open {
    display: flex;
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
</style>
