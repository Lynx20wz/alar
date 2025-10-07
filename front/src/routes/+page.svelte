<script lang="ts">
  import { getTranslate } from "@tolgee/svelte";

  const { t } = getTranslate();
</script>

<aside class="aside">
  <h5 class="aside-header">{$t("favorites")}</h5>

  
</aside>

<style lang="scss">
  :global(body) {
    font-family: "JetBrainsMono", sans-serif;
  }
  .aside {
    height: 1000px;
    width: 250px;
    background-color: var(--primary);
    padding: 10px;
    border-radius: 10px;

    &-header {
      text-align: center;
    }
  }
</style>
