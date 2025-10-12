<script lang="ts">
  import { page } from "$app/state";
  import Aside from "$lib/components/Aside.svelte";
  import UserCard from "$lib/components/UserCard.svelte";
  import { formatTimeAgo } from "$lib/utils";
  import { getTranslate, getTolgee } from "@tolgee/svelte";

  const { t } = getTranslate();
  const Tolgee = getTolgee(["language"]);
  const post = page.data.post;
  console.log(post.image);

  async function likePost() {
    const response = await fetch(`/api/posts/${post.id}/like`, {
      method: "POST",
    });
    if (response.ok) {
      const json = await response.json();
      post.is_liked = json.data;
      post.likes.total += json.data ? 1 : -1;
    }
  }
</script>

<svelte:head>
  <title>{post.title}</title>
</svelte:head>

<div class="container df">
  <Aside />
  <div class="content df">
    <div class="post df">
      <div class="post__header df">
        <h4 class="post__title">{post.title}</h4>
        <UserCard user={post.author} />
      </div>
      {#if post.hasImage}
        <img src="/api/posts/{post.id}/image" alt="post" />
      {/if}
      <h5 class="post__content">{post.content}</h5>
      <div class="stats df">
        <div class="stats__counters df">
          <h5 class="stats__counter df">
            <button
              class="stats__button df"
              aria-label="like post"
              onclick={likePost}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="30"
                height="27"
                viewBox="0 0 30 27"
                fill="none"
              >
                <path
                  class:isLiked={post.is_liked}
                  d="M5.45455 10.8V27H0V10.8H5.45455ZM10.9091 27C10.1858 27 9.49208 26.7155 8.98062 26.2092C8.46916 25.7028 8.18182 25.0161 8.18182 24.3V10.8C8.18182 10.0575 8.48182 9.3825 8.98636 8.8965L17.9591 0L19.4045 1.431C19.7727 1.7955 20.0045 2.295 20.0045 2.8485L19.9636 3.2805L18.6682 9.45H27.2727C27.996 9.45 28.6897 9.73446 29.2012 10.2408C29.7127 10.7472 30 11.4339 30 12.15V14.85C30 15.201 29.9318 15.525 29.8091 15.8355L25.6909 25.353C25.2818 26.325 24.3136 27 23.1818 27H10.9091Z"
                  fill="var(--secondary)"
                />
              </svg>
            </button>
            {post.likes.total}
          </h5>
          <h5 class="stats__counter df">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="30"
              height="19"
              viewBox="0 0 30 19"
              fill="none"
            >
              <path
                fill-rule="evenodd"
                clip-rule="evenodd"
                d="M29.0009 9.50104L29.8949 9.06861V9.06445L29.8885 9.05821L29.8755 9.03327L29.8303 8.9501L29.658 8.65073C29.4477 8.30063 29.2242 7.95806 28.988 7.6237C28.1999 6.50717 27.2939 5.47253 26.2846 4.53638C23.859 2.29106 20.1258 0 14.9989 0C9.87634 0 6.14103 2.28898 3.71544 4.53638C2.70614 5.47253 1.80014 6.50717 1.01198 7.6237C0.692166 8.0791 0.395964 8.54953 0.124463 9.03327L0.111538 9.05821L0.10723 9.06445V9.06653C0.10723 9.06653 0.105076 9.06861 0.999052 9.50104L0.105076 9.06653C0.0359583 9.20129 0 9.34963 0 9.5C0 9.65037 0.0359583 9.79871 0.105076 9.93347L0.102922 9.93763L0.109384 9.94387L0.122309 9.96882C0.18948 10.0987 0.261329 10.2263 0.337725 10.3514C1.2653 11.8636 2.4 13.2483 3.71114 14.4678C6.13887 16.7131 9.87203 19 14.9989 19C20.1237 19 23.859 16.7131 26.2867 14.4657C27.2941 13.5284 28.1993 12.4939 28.988 11.3784C29.2901 10.9492 29.5711 10.5065 29.8303 10.052L29.8755 9.96882L29.8885 9.94387L29.8928 9.93763V9.93555C29.8928 9.93555 29.8949 9.93347 29.0009 9.50104ZM29.0009 9.50104L29.8949 9.93555C29.964 9.80079 30 9.65245 30 9.50208C30 9.35171 29.964 9.20337 29.8949 9.06861L29.0009 9.50104ZM14.8697 6.30769C13.9921 6.30769 13.1505 6.64413 12.53 7.243C11.9095 7.84187 11.5609 8.65411 11.5609 9.50104C11.5609 10.348 11.9095 11.1602 12.53 11.7591C13.1505 12.3579 13.9921 12.6944 14.8697 12.6944C15.7472 12.6944 16.5888 12.3579 17.2093 11.7591C17.8299 11.1602 18.1785 10.348 18.1785 9.50104C18.1785 8.65411 17.8299 7.84187 17.2093 7.243C16.5888 6.64413 15.7472 6.30769 14.8697 6.30769ZM9.56614 9.50104C9.56614 8.14242 10.1254 6.83946 11.1208 5.87877C12.1162 4.91809 13.4663 4.37838 14.874 4.37838C16.2817 4.37838 17.6318 4.91809 18.6272 5.87877C19.6226 6.83946 20.1818 8.14242 20.1818 9.50104C20.1818 10.8597 19.6226 12.1626 18.6272 13.1233C17.6318 14.084 16.2817 14.6237 14.874 14.6237C13.4663 14.6237 12.1162 14.084 11.1208 13.1233C10.1254 12.1626 9.56614 10.8597 9.56614 9.50104Z"
                fill="#7072AE"
              />
            </svg>{post.views}
          </h5>
        </div>
        <p class="stats__date">
          {formatTimeAgo(
            new Date(post.created_at),
            $Tolgee.getLanguage()?.toString()
          )}
        </p>
      </div>
    </div>
    <div class="comments df">
      <input
        class="comment__input"
        type="text"
        placeholder={$t("ph-comment")}
      />
      {#each post.comments as comment}
        <div class="comment df">
          <div class="comment__info df">
            <UserCard user={comment.author} />
            <p class="comment__date">
              {formatTimeAgo(
                new Date(comment.created_at),
                $Tolgee.getLanguage()?.toString()
              )}
            </p>
          </div>
          <p class="comment__content">{comment.content}</p>
        </div>
      {/each}
    </div>
  </div>
</div>

<style lang="scss">
  .isLiked {
    filter: brightness(1.5);
  }
  .container {
    gap: 15px;
    padding: 20px;
    flex-direction: row;
    align-items: start;
    justify-content: start;
  }

  .content {
    flex-direction: column;
    align-items: stretch;
    flex-grow: 1;
    gap: 10px;
  }
  .post {
    padding: 10px;
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
    border-radius: 10px;
    background: var(--primary);

    &__header {
      align-self: stretch;
      justify-content: space-between;
    }
    &__content {
      color: var(--grayA1);
    }
  }

  .stats {
    justify-content: space-between;
    align-self: stretch;
    align-items: flex-end;
    &__button {
      background: none;
      border: none;
    }
    &__counters {
      gap: 10px;
      color: var(--secondary);
    }
    &__counter {
      gap: 5px;
    }
    &__date {
      color: var(--secondary);
    }
  }

  .comments {
    flex-direction: column;
    justify-content: flex-start;
    gap: 10px;
    & > * {
      align-self: stretch;
    }
  }

  .comment {
    flex-direction: column;
    align-items: flex-start;
    background-color: var(--primary);
    border-radius: 10px;
    padding: 10px;
    gap: 10px;
    &__info {
      align-self: stretch;
      justify-content: space-between;
    }
    &__date {
      color: var(--secondary);
    }
    &__content {
      color: var(--grayA1);
    }
    &__input {
      transition: outline 50ms;
      border: none;
      background-color: var(--primary);
      padding: 10px;
      border-radius: 10px;
      height: 50px;
      color: white;
      &:focus {
        outline: 2px solid var(--secondary);
      }
      &::placeholder {
        color: var(--grayA1);
      }
    }
  }
</style>
