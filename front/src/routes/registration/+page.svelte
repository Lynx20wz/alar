<script lang="ts">
  import { getTranslate } from "@tolgee/svelte";
  import Alert from "$lib/components/Alert.svelte";

  let continueRegistration = $state(false);
  let userExist = $state(false);
  let alert: Alert;

  const { t } = getTranslate();

  async function handleRegistration(e: Event) {
    e.preventDefault();
    const formData = new FormData(e.target as HTMLFormElement);

    if (!continueRegistration) {
      const response = await fetch(
        `/api/exists?username=${formData.get("username")}`,
        { method: "GET" }
      );

      if (response.ok) {
        const json = await response.json();
        if (json.exists) {
          userExist = true;
          setTimeout(() => (userExist = false), 3000);
        } else {
          continueRegistration = true;
          (
            document.querySelector('input[name="username"]') as HTMLInputElement
          ).focus();
        }
      } else alert.show("User already exists");
    } else {
      const data = new FormData();

      data.append("username", formData.get("username")!);
      data.append("password", formData.get("password")!);
      data.append("email", formData.get("email")!);

      if ((formData.get("avatar") as File).name) {
        data.append("avatar", formData.get("avatar") as File);
      }
      if ((formData.get("banner") as File).name) {
        data.append("banner", formData.get("banner") as File);
      }

      const response = await fetch("/api/user", {
        method: "POST",
        body: data,
      });

      if (response.ok) {
        const json = await response.json();
        localStorage.setItem("auth_token", json.token);
        localStorage.setItem("username", json.username);
        window.location.href = "/";
      } 
    }
  }

  $effect(() => (userExist ? alert.show() : alert.hide()));

  async function handleMedia(event: Event) {
    const file = (event.target as HTMLInputElement).files![0];
    const block = document.querySelector(
      `.extra-block__${event.target?.name?.split("-")[0]}`
    ) as HTMLDivElement;

    const fileURL = URL.createObjectURL(file);

    block!.style.backgroundImage = `url(${fileURL})`;
    block!.style.backgroundColor = "transparent";
    block!.classList.remove("upload");
  }

  async function checkUsername() {}
</script>

<Alert bind:this={alert} type="error" message="User already exist" />

<form class="df" onsubmit={(e) => handleRegistration(e)}>
  <div class="avatar df">
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width="131"
      height="58"
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
    <h5>{$t("registrationSlogan")}</h5>
  </div>
  <div class="extra-block df" class:visible={continueRegistration}>
    <div class="extra-block__media df">
      <label for="avatar-upload" class="extra-block__avatar upload df">
        <svg
          style="opacity: 0;"
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="30"
          viewBox="0 0 24 30"
          fill="none"
        >
          <path
            d="M0 30H24V26.4706H0V30ZM0 12.3529H6.85714V22.9412H17.1429V12.3529H24L12 0L0 12.3529Z"
            fill="#666890"
          />
        </svg>
      </label>
      <input
        onchange={(e) => handleMedia(e)}
        class="hidden"
        id="avatar-upload"
        type="file"
        accept="image/*"
        name="avatar"
      />

      <label for="banner-upload" class="extra-block__banner upload df">
        <svg
          style="opacity: 0;"
          xmlns="http://www.w3.org/2000/svg"
          width="24"
          height="30"
          viewBox="0 0 24 30"
          fill="none"
        >
          <path
            d="M0 30H24V26.4706H0V30ZM0 12.3529H6.85714V22.9412H17.1429V12.3529H24L12 0L0 12.3529Z"
            fill="#666890"
          />
        </svg>
      </label>
      <input
        onchange={(e) => handleMedia(e)}
        class="hidden"
        id="banner-upload"
        type="file"
        accept="image/*"
        name="banner"
      />
    </div>
    <input
      class="input"
      type="email"
      name="email"
      autocomplete="email"
      placeholder={$t("ph-email")}
      required={continueRegistration}
    />
  </div>
  <div class="controls df">
    <div class="inputs df">
      <input
        class="input"
        type="text"
        name="username"
        autocomplete="username"
        placeholder={$t("ph-username")}
        required
      />
      <input
        class="input"
        type="password"
        name="password"
        autocomplete="current-password"
        placeholder={$t("ph-password")}
        required
      />
    </div>
    <button class="df hscale" type="submit">{$t("btn-signUp")}</button>
    <a aria-label="registration" href="/login">{$t("l-login")}</a>
  </div>
</form>

<!-- <button
  style="position: fixed; top: 0;"
  onclick={() => (continueRegistration = !continueRegistration)}>test</button
> -->

<!-- <button
  style="position: fixed; top: 0;"
  onclick={() => (alert.show())}>test</button
> -->

<style lang="scss">
  :global(body) {
    display: flex;
    align-items: center;
    justify-content: center;
  }

  form {
    flex-direction: column;
    width: 550px;
    gap: 16px;
  }

  .avatar {
    gap: 10px;
    flex-direction: column;
    width: 100%;
  }

  .controls {
    flex-direction: column;
    gap: 10px;
    width: 100%;
    align-items: flex-end;
  }

  .extra-block {
    flex-direction: column;
    gap: 10px;
    width: 100%;
    opacity: 0;
    height: 0;
    margin: -8px;
    transform: scaleY(0);
    transition:
      opacity 300ms ease-out,
      transform 300ms ease-out,
      height 300ms ease-out,
      margin 300ms ease-out;

    &.visible {
      margin: 0;
      opacity: 1;
      height: 152px;
      transform: scaleY(1);
    }

    &__media {
      gap: 5px;
      width: 100%;
      height: 100px;
    }

    &__avatar {
      width: 100px;
      height: 100px;
      background-color: var(--gray33);
      background-size: 100px 100px;
      border-radius: 50%;
      flex-shrink: 0;
      overflow: hidden;
    }

    &__banner {
      width: 100%;
      height: 100%;
      background-color: var(--gray33);
    }
  }

  .inputs {
    flex-direction: column;
    width: 100%;
    gap: 6px;
  }

  .input {
    width: 100%;
    padding: 5px 10px;
    border: 1px solid var(--white);
    border-radius: 10px;
    background-color: transparent;
    color: var(--white);
    font-size: 20px;

    &::placeholder {
      color: var(--white);
    }
  }

  button {
    padding: 10px 5px;
    gap: 10px;
    align-self: stretch;
    border-radius: 10px;
  }

  .upload {
    transition: filter 200ms;

    & svg {
      opacity: 0;
      transition: opacity 200ms;
    }

    &:hover {
      & svg {
        opacity: 1 !important;
      }
      filter: brightness(0.8);
    }
  }
</style>
