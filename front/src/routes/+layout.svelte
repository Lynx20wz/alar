<script lang="ts">
  import "./styles/global.scss";
  import {
    TolgeeProvider,
    Tolgee,
    DevTools,
    LanguageStorage,
  } from "@tolgee/svelte";
  import { FormatIcu } from "@tolgee/format-icu";
  import { isAuthenticated } from "$lib/auth";
  import { onMount } from "svelte";

  onMount(async () => {
    await isAuthenticated();
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
  <main class="page">
    <slot />
  </main>
</TolgeeProvider>

<style lang="scss">
</style>
