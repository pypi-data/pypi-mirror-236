from PIL import Image
from py_book_util import util
from py_book_util.page_recognizer import PageRecognizer
from py_book_util.image_recognizer import ImageRecognizer
from myst_nb import glue
from IPython.display import Markdown
import os


class CrossPageRecognizer(PageRecognizer):
    def __init__(
        self, cur_pages_dir, cur_page_idx, cur_page_width=2561, cur_page_height=1206
    ):
        super().__init__(cur_pages_dir, cur_page_idx, cur_page_width, cur_page_height)
        page_tokens = cur_page_idx.split("_")
        page_idx_prefix = ""
        next_page_idx_number = 0
        if len(page_tokens) > 1:
            page_idx_prefix = page_tokens[0]
            next_page_idx_number = int(page_tokens[1]) + 1
            self.next_page_idx = "%s_%06d" % (page_idx_prefix, next_page_idx_number)
        else:
            next_page_idx_number = int(page_tokens[0]) + 1
            self.next_page_idx = "%06d" % next_page_idx_number
        print(self.next_page_idx)
        if os.path.exists(self.next_img_file()):
            img = Image.open(self.next_img_file())
            self.next_img_width = img.width
            self.next_img_height = img.height
        else:
            print("Can not find %s!" % self.next_img_file())
        if os.path.exists(self.cross_img_file()) is False:
            assert self.page_width == self.next_img_width
            new_img_height = self.page_height + self.next_img_height
            new_image = Image.new("RGB", (self.page_width, new_img_height))
            from_image = Image.open(self.cur_img_file())
            new_image.paste(from_image, (0, 0))
            from_image = Image.open(self.next_img_file())
            new_image.paste(from_image, (0, self.page_height))
            new_image.save(self.cross_img_file())
        if os.path.exists(self.cross_img_file()):
            img = Image.open(self.cross_img_file())
            self.cross_img_width = img.width
            self.cross_img_height = img.height

    def cross_img_file(self):
        return "%s/%s_%s.png" % (self.pages_dir, self.page_idx, self.next_page_idx)

    def next_img_file(self):
        return "%s/%s.png" % (self.pages_dir, self.next_page_idx)

    def recognize_rect_impl(
        self,
        cur_key_word,
        crop_img_top,
        crop_img_bottom,
        crop_img_left,
        crop_img_right,
        post_replace={},
        flag_force=False,
        ratio="2.0",
        flag_autocrop=True,
        app_name="img2txt",
    ):
        using_img_file = self.cur_img_file()
        if crop_img_bottom < 0:
            crop_img_bottom = crop_img_bottom + self.next_img_height
            using_img_file = self.cross_img_file()
        cur_rec = ImageRecognizer(
            "%s.png" % cur_key_word,
            crop_img_top,
            crop_img_bottom,
            crop_img_left,
            crop_img_right,
            using_img_file,
            self.dst_img_dir(),
            flag_force,
            ratio,
            flag_autocrop,
            app_name,
        )
        cur_rec_data = cur_rec.recognize_text(app_name)
        for single_replace_key in post_replace:
            cur_rec_data["recognize_text"] = cur_rec_data["recognize_text"].replace(
                single_replace_key, post_replace[single_replace_key]
            )  # ("\u2014", "-")
        glue(cur_key_word, Markdown(cur_rec_data["recognize_text"]))
        self.page_elements[cur_key_word] = cur_rec_data
        return cur_rec


class CrossPrevPageRecognizer(PageRecognizer):
    def __init__(
        self, cur_pages_dir, cur_page_idx, cur_page_width=2561, cur_page_height=1206
    ):
        super().__init__(cur_pages_dir, cur_page_idx, cur_page_width, cur_page_height)
        page_tokens = cur_page_idx.split("_")
        page_idx_prefix = ""
        prev_page_idx_number = 0
        if len(page_tokens) > 1:
            page_idx_prefix = page_tokens[0]
            prev_page_idx_number = int(page_tokens[1]) - 1
            assert prev_page_idx_number > 0
            self.prev_page_idx = "%s_%06d" % (page_idx_prefix, prev_page_idx_number)
        else:
            prev_page_idx_number = int(page_tokens[0]) - 1
            assert prev_page_idx_number > 0
            self.prev_page_idx = "%06d" % prev_page_idx_number
        print(self.prev_page_idx)
        if os.path.exists(self.prev_img_file()):
            img = Image.open(self.prev_img_file())
            self.prev_img_width = img.width
            self.prev_img_height = img.height
        else:
            print("Can not find %s!" % self.prev_img_file())
        if os.path.exists(self.cross_img_file()) is False:
            assert self.page_width == self.prev_img_width
            new_img_height = self.page_height + self.prev_img_height
            new_image = Image.new("RGB", (self.page_width, new_img_height))
            from_image = Image.open(self.prev_img_file())
            new_image.paste(from_image, (0, 0))
            from_image = Image.open(self.cur_img_file())
            new_image.paste(from_image, (0, self.prev_img_height))
            new_image.save(self.cross_img_file())
        if os.path.exists(self.cross_img_file()):
            img = Image.open(self.cross_img_file())
            self.cross_img_width = img.width
            self.cross_img_height = img.height

    def cross_img_file(self):
        return "%s/%s_%s.png" % (self.pages_dir, self.prev_page_idx, self.page_idx)

    def prev_img_file(self):
        return "%s/%s.png" % (self.pages_dir, self.prev_page_idx)

    def recognize_rect_impl(
        self,
        cur_key_word,
        crop_img_top,
        crop_img_bottom,
        crop_img_left,
        crop_img_right,
        post_replace={},
        flag_force=False,
        ratio="2.0",
        flag_autocrop=True,
        app_name="img2txt",
    ):
        using_img_file = self.cur_img_file()
        print(
            "crop_img_top is %d crop_img_bottom is %d" % (crop_img_top, crop_img_bottom)
        )
        if crop_img_top < 0:
            crop_img_top = crop_img_top + self.prev_img_height
            # crop_img_bottom = crop_img_bottom + self.prev_img_height
            print(
                "crop_img_top is %d crop_img_bottom is %d"
                % (crop_img_top, crop_img_bottom)
            )
            using_img_file = self.cross_img_file()
        cur_rec = ImageRecognizer(
            "%s.png" % cur_key_word,
            crop_img_top,
            crop_img_bottom,
            crop_img_left,
            crop_img_right,
            using_img_file,
            self.dst_img_dir(),
            flag_force,
            ratio,
            flag_autocrop,
            app_name,
        )
        cur_rec_data = cur_rec.recognize_text(app_name)
        for single_replace_key in post_replace:
            cur_rec_data["recognize_text"] = cur_rec_data["recognize_text"].replace(
                single_replace_key, post_replace[single_replace_key]
            )  # ("\u2014", "-")
        glue(cur_key_word, Markdown(cur_rec_data["recognize_text"]))
        self.page_elements[cur_key_word] = cur_rec_data
        return cur_rec
