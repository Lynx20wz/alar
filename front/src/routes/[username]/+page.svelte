<script lang="ts">
  import { getTranslate } from "@tolgee/svelte";
  import { page } from "$app/state";
  import type { PageProps } from "./$types";

  const user = page.data.user;
  const { data }: PageProps = $props();
  const { visited_user } = data;
  const isSelf = user?.username === visited_user?.username;

  let avatarEl: HTMLImageElement | undefined = $state(undefined);
  let bannerEl: HTMLImageElement | undefined = $state(undefined);

  async function handleMedia(e: Event) {
    const formData = new FormData();
    const targetEl = e.target as HTMLInputElement;
    const elName = targetEl.id.split("-")[0];
    const file = targetEl.files![0];

    formData.append("file", file);
    const response = await fetch(
      `/api/users${elName}/${visited_user?.username}`,
      {
        method: "POST",
        body: formData,
      }
    );

    if (response.ok && avatarEl && elName === "avatar") {
      avatarEl.src = `/api/users${elName}/${visited_user?.username}`;
    } else if (response.ok && bannerEl && elName === "banner") {
      bannerEl.src = `/api/users${elName}/${visited_user?.username}`;
    }
  }

  const { t } = getTranslate();
</script>

<svelte:head>
  <title>{visited_user?.username}</title>
</svelte:head>

{#snippet media(element: string)}
  <img
    class="banner__{element}"
    src="/api/users/{element}/{visited_user?.username}"
    alt={element}
  />
{/snippet}

<main class="content">
  <div class="banner">
    {#if isSelf}
      <label for="banner-upload">{@render media("banner")}</label>
      <input
        id="banner-upload"
        type="file"
        class="hidden"
        accept="image/*"
        onchange={(e) => handleMedia(e)}
      />
    {:else}
      {@render media("banner")}
    {/if}
    <div class="banner-elements df">
      <div class="banner__user-time"><h5>15:42</h5></div>
    </div>
    {#if isSelf}
      <label for="avatar-upload">{@render media("avatar")}</label>
      <input
        id="avatar-upload"
        type="file"
        class="hidden"
        accept="image/*"
        onchange={(e) => handleMedia(e)}
      />
    {:else}
      {@render media("avatar")}
    {/if}
  </div>
  <div class="user-info df">
    <div class="user-info__main df">
      <div class="user-info__inner df">
        <h1 class="user-info__username">{visited_user?.username}</h1>
        <h6 class="user-info__followers">
          <span class="text-logo"
            ><svg
              xmlns="http://www.w3.org/2000/svg"
              width="36"
              height="24"
              viewBox="0 0 36 24"
              fill="none"
            >
              <path
                d="M24.5455 10.2857C27.2618 10.2857 29.4382 7.98857 29.4382 5.14286C29.4382 2.29714 27.2618 0 24.5455 0C21.8291 0 19.6364 2.29714 19.6364 5.14286C19.6364 7.98857 21.8291 10.2857 24.5455 10.2857ZM11.4545 10.2857C14.1709 10.2857 16.3473 7.98857 16.3473 5.14286C16.3473 2.29714 14.1709 0 11.4545 0C8.73818 0 6.54545 2.29714 6.54545 5.14286C6.54545 7.98857 8.73818 10.2857 11.4545 10.2857ZM11.4545 13.7143C7.64182 13.7143 0 15.72 0 19.7143V22.2857C0 23.2286 0.736364 24 1.63636 24H21.2727C22.1727 24 22.9091 23.2286 22.9091 22.2857V19.7143C22.9091 15.72 15.2673 13.7143 11.4545 13.7143ZM24.5455 13.7143C24.0709 13.7143 23.5309 13.7486 22.9582 13.8C22.9909 13.8171 23.0073 13.8514 23.0236 13.8686C24.8891 15.2914 26.1818 17.1943 26.1818 19.7143V22.2857C26.1818 22.8857 26.0673 23.4686 25.8873 24H34.3636C35.2636 24 36 23.2286 36 22.2857V19.7143C36 15.72 28.3582 13.7143 24.5455 13.7143Z"
                fill="var(--secondary)"
              />
            </svg></span
          >
          {$t("followers-counter", { count: visited_user?.follows.total })}
        </h6>
      </div>
      <p class="bio">{visited_user?.bio}</p>
    </div>
    <div class="social df">
      {#each visited_user?.social_links as social}
        <a href={social.url} target="_blank" class="social__link">
          <img
            src={`https://favicon.is/${
              new URL(social.url).hostname
            }?larger=true`}
            alt={social.platform}
          />
        </a>
      {/each}
    </div>
  </div>
  <div class="container"></div>
</main>

<style lang="scss">
  :global(.content) {
    font-family: "JetBrainsMono", sans-serif;
  }
  .banner {
    position: relative;
    &-elements {
      position: absolute;
      bottom: 5px;
      right: 40px;
      gap: 5px;
    }

    &__banner {
      width: 100%;
      height: 300px;
      object-fit: cover;
      object-position: center 50%;
    }

    &__user-time {
      background-color: var(--primary);
      padding: 4px 10px;
    }

    &__avatar {
      position: absolute;
      bottom: -16px;
      left: 40px;
      width: 200px;
      height: 200px;
      border-radius: 50%;
    }
  }
  .container {
    padding: 20px 40px;
  }
  .user-info {
    justify-content: space-between;
    margin-inline: 240px 40px;
    &__main {
      align-items: start;
      flex-direction: column;
    }
    &__inner {
      gap: 10px;
      align-items: baseline;
    }
    &__followers {
      color: var(--secondary);
    }
  }
  .social {
    background-color: var(--primary);
    padding: 15px 20px;
    gap: 20px;
    border-radius: 15px;

    &__link {
      width: 50px;
    }
  }
</style>
