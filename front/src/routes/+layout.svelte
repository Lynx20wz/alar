<script lang="ts">
  import "./styles/global.scss";
  import {
    TolgeeProvider,
    Tolgee,
    DevTools,
    LanguageStorage,
  } from "@tolgee/svelte";
  import { FormatIcu } from "@tolgee/format-icu";
  import isAuthenticated from "$lib/auth";
  import { onMount } from "svelte";
  import Header from "$lib/components/Header.svelte";
  import { publicRouter } from "$lib/config";

  let isPublicRoute = false;

  onMount(async () => {
    isPublicRoute = publicRouter.includes(window.location.pathname);
    if (!isPublicRoute) {
      await isAuthenticated();
    }
  });

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
  <main class="page df">
    {#if !isPublicRoute}
      <Header />
    {/if}
    <slot />
  </main>
</TolgeeProvider>

<style lang="scss">
  .page {
    width: 100%;
    flex-direction: column;
  }
</style>
