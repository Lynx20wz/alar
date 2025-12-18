<script lang="ts">
  import {
    TolgeeProvider,
    Tolgee,
    DevTools,
    LanguageStorage,
  } from "@tolgee/svelte";
  import { FormatIcu } from "@tolgee/format-icu";
  import { isPublicRoute } from "$lib/utils";

  import "./styles/global.scss";
  import Header from "$lib/components/Header.svelte";

  const tolgee = Tolgee()
    .use(DevTools())
    .use(FormatIcu())
    .use(LanguageStorage())
    .init({
      availableLanguages: ["en", "ru-RU"],
      defaultLanguage: "en",
      apiUrl: import.meta.env.VITE_TOLGEE_API_URL,
      apiKey: import.meta.env.VITE_TOLGEE_API_KEY,
    });
</script>

<TolgeeProvider {tolgee}>
  <main class="page">
    {#if !isPublicRoute(window.location.pathname)}
      <Header />
    {/if}
    <div
      class="content"
      class:container={!isPublicRoute(window.location.pathname)}
    >
      <slot />
    </div>
  </main>
</TolgeeProvider>

<style lang="scss">
  .page {
    width: 100%;
    flex-direction: column;
  }

  .container {
    margin-top: 64px;
  }
</style>
