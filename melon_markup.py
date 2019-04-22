class FormatTag():
    def __init__(self, name, start, end, output_template):
        self.name = name
        self.start = start
        self.end = end
        self.output_template = output_template
        self.openings = []
        self.net_change = len(self.output_template.format(value="")) - len(self.start) - len(self.end)

    def close(self, unformatted, end_pos):
        if self.openings:
            pre_text = unformatted[:self.openings[-1]]
            post_text = unformatted[end_pos + len(self.end):]
            open_tag_end_pos = self.openings[-1] + len(self.start)
            interior = unformatted[open_tag_end_pos:end_pos]
            formatted = self.output_template.format(value=interior)
            self.openings = self.openings[:-1]
            return pre_text + formatted + post_text
        else:
            return unformatted

    def adjust_openings(self, pos, adjustment):
        for i, o in enumerate(self.openings):
            if o > pos:
                self.openings[i] += adjustment


def create_tags():
    tags = []

    name = "bold"
    start = "[b]"
    end = "[/b]"
    output_template = "<strong>{value}</strong>"

    bold = FormatTag(name=name, start=start, end=end, output_template=output_template)
    tags.append(bold)

    name = "italics"
    start = "[i]"
    end = "[/i]"
    output_template = "<em>{value}</em>"

    italics = FormatTag(name=name, start=start, end=end, output_template=output_template)
    tags.append(italics)

    name = "url"
    start = "[url]"
    end = "[/url]"
    output_template = "<a href={value}>{value}</a>"

    url = FormatTag(name=name, start=start, end=end, output_template=output_template)
    tags.append(url)

    return tags


tags = create_tags()


def parse(s):
    pos = 0
    while True:
        for tag in tags:
            if s[pos:].startswith(tag.start):
                tag.openings.append(pos)
                pos += len(tag.start)
                break
            elif s[pos:].startswith(tag.end):
                s = tag.close(s, pos)
                for stag in tags:
                    stag.adjust_openings(pos, tag.net_change)
                pos += tag.net_change + len(tag.end)
                break
        else:
            pos += 1

        if pos > len(s):
            return s
