<script lang="ts">
  import { getTranslate } from "@tolgee/svelte";
  import type { User } from "$lib/types/User";
  import { getAvatarUrl, getUser } from "$lib/user";
  import { onMount } from "svelte";

  const { t } = getTranslate();

  let avatar: string | undefined;
  let user: User | undefined;

  onMount(async () => {
    avatar = await getAvatarUrl();
    user = await getUser();
  });
</script>

<header class="header df">
  <div class="header__left-block df">
    <a aria-label="home" href="/">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="100"
        height="44"
        viewBox="0 0 131 58"
        fill="none"
      >
        <path
          fill-rule="evenodd"
          clip-rule="evenodd"
          d="M30.7311 0.00215325H18.3291L0 57.9999L6.6666 58L11.2301 42.5868H24.3452V58L30.7311 57.9999V0.00215325ZM24.3452 37.912V5.72106C20.3504 5.72106 16.6934 23.5517 12.7552 37.912H24.3452Z"
          fill="white"
        />
        <path
          fill-rule="evenodd"
          clip-rule="evenodd"
          d="M41.77 54.6631C39.4705 52.3856 38.3208 49.393 38.3208 45.6854V0.00216083H45.5401V45.6854C45.5401 49.5 49.5 51.4797 51.7254 51.4871L65.2551 0.000728799H74.9611L88.4512 51.6078L95.545 51.6311V0H113.593C117.069 0 120.118 0.715042 122.738 2.14513C125.358 3.52224 127.39 5.4555 128.834 7.94491C130.278 10.4343 131 13.3475 131 16.6843C131 20.6038 129.984 23.9671 127.952 26.7744C125.92 29.5816 123.219 31.5413 119.85 32.6536L131 57.9978L50.0224 57.9675C46.6416 57.7697 43.8909 56.6683 41.77 54.6631ZM61.2444 42.5854H78.9719L81.2198 51.584L59.0147 51.511L61.2444 42.5854ZM77.4478 36.5473H62.6882L67.1803 18.5918C68.0359 15.255 68.7044 12.4478 69.1856 10.1702C69.6669 7.89267 69.961 6.40962 70.068 5.72106C70.1749 6.40962 70.4691 7.89267 70.9504 10.1702C71.4317 12.4478 72.1001 15.2814 72.9557 18.6713L77.4478 36.5473ZM102.684 33.3686H112.39L120.935 51.7146L102.684 51.6546V33.3686ZM113.593 26.9332H102.684V6.43538H113.593C116.588 6.43538 118.995 7.36228 120.813 9.2161C122.631 11.0699 123.54 13.5593 123.54 16.6843C123.54 19.7563 122.631 22.2458 120.813 24.1525C118.995 26.0063 116.588 26.9332 113.593 26.9332Z"
          fill="white"
        />
      </svg>
    </a>
    <div class="header__icons df">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="30"
        height="30"
        viewBox="0 0 30 30"
        fill="none"
      >
        <path
          d="M29 24.2857V25.7143H1V24.2857L4.11111 21.4286V12.8571C4.11111 8.42857 7.26889 4.52857 11.8889 3.27143V2.85714C11.8889 2.09938 12.2167 1.37266 12.8001 0.836838C13.3836 0.301019 14.1749 0 15 0C15.8251 0 16.6164 0.301019 17.1999 0.836838C17.7833 1.37266 18.1111 2.09938 18.1111 2.85714V3.27143C22.7311 4.52857 25.8889 8.42857 25.8889 12.8571V21.4286L29 24.2857ZM18.1111 27.1429C18.1111 27.9006 17.7833 28.6273 17.1999 29.1632C16.6164 29.699 15.8251 30 15 30C14.1749 30 13.3836 29.699 12.8001 29.1632C12.2167 28.6273 11.8889 27.9006 11.8889 27.1429"
          fill="#7072AE"
        />
      </svg>
      <svg
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
      </svg>
    </div>
  </div>
  <div class="header__search df">
    <label for="search">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="30"
        height="30"
        viewBox="0 0 33 34"
        fill="none"
      >
        <path
          d="M31.5 32L21.5 22M1.5 13.6667C1.5 15.1988 1.80177 16.7158 2.38807 18.1313C2.97438 19.5468 3.83374 20.8329 4.91709 21.9162C6.00044 22.9996 7.28656 23.859 8.70203 24.4453C10.1175 25.0316 11.6346 25.3333 13.1667 25.3333C14.6988 25.3333 16.2158 25.0316 17.6313 24.4453C19.0468 23.859 20.3329 22.9996 21.4162 21.9162C22.4996 20.8329 23.359 19.5468 23.9453 18.1313C24.5316 16.7158 24.8333 15.1988 24.8333 13.6667C24.8333 12.1346 24.5316 10.6175 23.9453 9.20203C23.359 7.78656 22.4996 6.50044 21.4162 5.41709C20.3329 4.33374 19.0468 3.47438 17.6313 2.88807C16.2158 2.30177 14.6988 2 13.1667 2C11.6346 2 10.1175 2.30177 8.70203 2.88807C7.28656 3.47438 6.00044 4.33374 4.91709 5.41709C3.83374 6.50044 2.97438 7.78656 2.38807 9.20203C1.80177 10.6175 1.5 12.1346 1.5 13.6667Z"
          stroke="#7072AE"
          stroke-width="3"
          stroke-linecap="round"
          stroke-linejoin="round"
        />
      </svg>
    </label>
    <input
      id="search"
      class="input"
      type="text"
      name="search"
      placeholder={$t("ph-search")}
    />
  </div>
  <a
    href={`/${user?.username}`}
    aria-label="profile"
    class="header__profile"
  >
    <img class="header__avatar" src={avatar || ""} alt="avatar" />
  </a>
</header>

<style lang="scss">
  .header {
    position: fixed;
    top: 0;
    align-items: center;
    width: 100%;
    justify-content: space-between;
    background-color: var(--primary);
    height: 64px;
    padding: 10px 20px;

    &__left-block {
      gap: 20px;
    }

    &__icons {
      gap: 5px;
      align-items: center;
    }

    &__search {
      width: 480px;
      height: 44px;
      background-color: var(--bg);
      border-radius: 12px;
      padding: 10px;
      gap: 8px;
      cursor: pointer;
      align-items: center;

      & label {
        height: 30px;
        &:active {
          transform: scale(0.9);
        }
      }


      &:focus-within {
        outline: 1px solid var(--secondary);
      }

      & input {
        width: 100%;
        // height: 100%;
        background-color: transparent;
        border: none;
        color: var(--secondary);
        font-size: 20px;
        position: relative;
        &::placeholder {
          color: var(--secondary);
        }
        &:focus {
          outline: none;
        }
      }
    }

    &__profile {
      background-color: transparent;
    }

    &__avatar {
      height: 44px;
      aspect-ratio: 1;
      border-radius: 50%;
    }
  }
</style>
