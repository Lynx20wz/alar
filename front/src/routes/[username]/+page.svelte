<script lang="ts">
  import { getTranslate } from "@tolgee/svelte";
  import { page } from "$app/stores";
  import type { PageProps } from "./$types";

  const user = $page.data.user;
  const { data }: PageProps = $props();
  const { visited_user } = data;
  const isSelf = user?.username === visited_user?.username;

  const { t } = getTranslate();
</script>

<main class="content">
  <div class="banner">
    <img
      class="banner__media"
      src={`/api/user/banner/${visited_user?.username}`}
      alt="Banner"
    />
    <div class="banner-elements df">
      {#if isSelf}
        <button type="button" aria-label="Edit profile" class="banner__edit df">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="30"
            height="30"
            viewBox="0 0 30 30"
            fill="none"
          >
            <path
              d="M16.6667 0C17.0915 0.000471179 17.5001 0.163132 17.8089 0.454747C18.1178 0.746363 18.3037 1.14492 18.3286 1.56899C18.3535 1.99306 18.2155 2.41063 17.9429 2.73639C17.6702 3.06214 17.2835 3.27149 16.8617 3.32167L16.6667 3.33333H3.33333V26.6667H26.6667V13.3333C26.6671 12.9085 26.8298 12.4999 27.1214 12.1911C27.413 11.8822 27.8116 11.6963 28.2357 11.6714C28.6597 11.6465 29.0773 11.7845 29.4031 12.0571C29.7288 12.3298 29.9382 12.7165 29.9883 13.1383L30 13.3333V26.6667C30.0003 27.5076 29.6827 28.3176 29.1108 28.9342C28.539 29.5509 27.7553 29.9286 26.9167 29.9917L26.6667 30H3.33333C2.49237 30.0003 1.68239 29.6827 1.06575 29.1108C0.449118 28.539 0.0714057 27.7553 0.00833369 26.9167L1.67113e-07 26.6667V3.33333C-0.000265965 2.49237 0.317344 1.68239 0.889162 1.06575C1.46098 0.449118 2.24474 0.0714055 3.08333 0.00833352L3.33333 0H16.6667ZM27.0717 0.571667C27.3716 0.272753 27.7741 0.0992108 28.1973 0.0862865C28.6206 0.0733621 29.0329 0.222025 29.3505 0.502081C29.6681 0.782137 29.8672 1.17259 29.9073 1.59412C29.9475 2.01566 29.8257 2.43668 29.5667 2.77167L29.4283 2.93L12.9283 19.4283C12.6284 19.7272 12.2259 19.9008 11.8027 19.9137C11.3794 19.9266 10.9671 19.778 10.6495 19.4979C10.3319 19.2179 10.1328 18.8274 10.0927 18.4059C10.0525 17.9843 10.1743 17.5633 10.4333 17.2283L10.5717 17.0717L27.0717 0.571667Z"
              fill="#7072AE"
            />
          </svg>
        </button>
      {/if}
      <div class="banner__user-time"><h5>15:42</h5></div>
    </div>
    <img
      class="banner__avatar"
      src="/api/user/avatar/{visited_user?.username}"
      alt="Avatar"
    />
  </div>
  <div class="container">
    <div class="user-info df">
      <h1 class="user-info__username">{visited_user?.username}</h1>
      <p class="followers">
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
              fill="#7072AE"
            />
          </svg></span
        >
        {$t("followers-counter", { count: visited_user?.followers.length })}
      </p>
    </div>
  </div>
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

    &__media {
      width: 100%;
      height: 300px;
      object-fit: cover;
      object-position: center 50%;
    }

    &__user-time {
      background-color: var(--primary);
      padding: 4px 10px;
    }

    &__edit {
      background-color: var(--primary);
      padding: 4px 5px;
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
    gap: 10px;
  }
</style>
