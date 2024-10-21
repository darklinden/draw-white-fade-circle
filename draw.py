#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import os
import shutil
import sys
import datetime
import errno
import re

from PIL import Image, ImageDraw

half_pi = math.pi / 2


class EaseFuncType:
    Linear = "Linear"
    QuadraticEaseIn = "QuadraticEaseIn"
    QuadraticEaseOut = "QuadraticEaseOut"
    QuadraticEaseInOut = "QuadraticEaseInOut"
    CubicEaseIn = "CubicEaseIn"
    CubicEaseOut = "CubicEaseOut"
    CubicEaseInOut = "CubicEaseInOut"
    QuarticEaseIn = "QuarticEaseIn"
    QuarticEaseOut = "QuarticEaseOut"
    QuarticEaseInOut = "QuarticEaseInOut"
    QuinticEaseIn = "QuinticEaseIn"
    QuinticEaseOut = "QuinticEaseOut"
    QuinticEaseInOut = "QuinticEaseInOut"
    SineEaseIn = "SineEaseIn"
    SineEaseOut = "SineEaseOut"
    SineEaseInOut = "SineEaseInOut"


def linear_func(progress):
    return progress


def quadratic_ease_in_func(progress):
    return ease_in_power(progress, 2)


def quadratic_ease_out_func(progress):
    return ease_out_power(progress, 2)


def quadratic_ease_in_out_func(progress):
    return ease_in_out_power(progress, 2)


def cubic_ease_in_func(progress):
    return ease_in_power(progress, 3)


def cubic_ease_out_func(progress):
    return ease_out_power(progress, 3)


def cubic_ease_in_out_func(progress):
    return ease_in_out_power(progress, 3)


def quartic_ease_in_func(progress):
    return ease_in_power(progress, 4)


def quartic_ease_out_func(progress):
    return ease_out_power(progress, 4)


def quartic_ease_in_out_func(progress):
    return ease_in_out_power(progress, 4)


def quintic_ease_in_func(progress):
    return ease_in_power(progress, 5)


def quintic_ease_out_func(progress):
    return ease_out_power(progress, 5)


def quintic_ease_in_out_func(progress):
    return ease_in_out_power(progress, 5)


def sine_ease_in_func(progress):
    return math.sin(progress * half_pi - half_pi) + 1


def sine_ease_out_func(progress):
    return math.sin(progress * half_pi)


def sine_ease_in_out_func(progress):
    return (math.sin(progress * math.pi - half_pi) + 1) / 2


def ease_in_power(progress, power):
    return progress**power


def ease_out_power(progress, power):
    sign = -1 if power % 2 == 0 else 1
    return sign * ((progress - 1) ** power + sign)


def ease_in_out_power(progress, power):
    progress *= 2.0
    if progress < 1:
        return (progress**power) / 2.0
    else:
        sign = -1 if power % 2 == 0 else 1
        return (sign / 2.0) * (((progress - 2) ** power) + (sign * 2))


def get_scale_func(func_type: EaseFuncType):
    if func_type == EaseFuncType.Linear:
        return linear_func
    elif func_type == EaseFuncType.QuadraticEaseIn:
        return quadratic_ease_in_func
    elif func_type == EaseFuncType.QuadraticEaseOut:
        return quadratic_ease_out_func
    elif func_type == EaseFuncType.QuadraticEaseInOut:
        return quadratic_ease_in_out_func
    elif func_type == EaseFuncType.CubicEaseIn:
        return cubic_ease_in_func
    elif func_type == EaseFuncType.CubicEaseOut:
        return cubic_ease_out_func
    elif func_type == EaseFuncType.CubicEaseInOut:
        return cubic_ease_in_out_func
    elif func_type == EaseFuncType.QuarticEaseIn:
        return quartic_ease_in_func
    elif func_type == EaseFuncType.QuarticEaseOut:
        return quartic_ease_out_func
    elif func_type == EaseFuncType.QuarticEaseInOut:
        return quartic_ease_in_out_func
    elif func_type == EaseFuncType.QuinticEaseIn:
        return quintic_ease_in_func
    elif func_type == EaseFuncType.QuinticEaseOut:
        return quintic_ease_out_func
    elif func_type == EaseFuncType.QuinticEaseInOut:
        return quintic_ease_in_out_func
    elif func_type == EaseFuncType.SineEaseIn:
        return sine_ease_in_func
    elif func_type == EaseFuncType.SineEaseOut:
        return sine_ease_out_func
    elif func_type == EaseFuncType.SineEaseInOut:
        return sine_ease_in_out_func
    else:
        return linear_func


CIRCLE_SOLID_RADIUS = 100
CIRCLE_SOLID_COLOR = (255, 255, 255, 255)
CIRCLE_GRADIENT_RADIUS = 400
CIRCLE_GRADIENT_TO_COLOR = (255, 255, 255, 0)
CIRCLE_GRADIENT_EASE_FUNC = EaseFuncType.QuinticEaseInOut


def main():
    try:

        w = 2
        min_w = (CIRCLE_SOLID_RADIUS + CIRCLE_GRADIENT_RADIUS + 1) * 2

        while w < min_w:
            w *= 2

        print("w: ", w)

        img = Image.new("RGBA", (w, w), (0, 0, 0, 0))
        # draw solid stoke circle
        draw = ImageDraw.Draw(img)
        center = (w // 2, w // 2)
        print("center: ", center)
        left_top = (center[0] - CIRCLE_SOLID_RADIUS, center[1] - CIRCLE_SOLID_RADIUS)
        right_bottom = (
            center[0] + CIRCLE_SOLID_RADIUS,
            center[1] + CIRCLE_SOLID_RADIUS,
        )
        print("left_top: ", left_top)
        print("right_bottom: ", right_bottom)
        draw.ellipse(
            (left_top[0], left_top[1], right_bottom[0], right_bottom[1]),
            fill=CIRCLE_SOLID_COLOR,
            width=CIRCLE_SOLID_RADIUS,
        )

        # draw gradient circle
        for x in range(CIRCLE_GRADIENT_RADIUS).__reversed__():
            progress = x / CIRCLE_GRADIENT_RADIUS
            scale = get_scale_func(CIRCLE_GRADIENT_EASE_FUNC)(progress)
            color = (
                int(
                    CIRCLE_SOLID_COLOR[0]
                    + (CIRCLE_GRADIENT_TO_COLOR[0] - CIRCLE_SOLID_COLOR[0]) * scale
                ),
                int(
                    CIRCLE_SOLID_COLOR[1]
                    + (CIRCLE_GRADIENT_TO_COLOR[1] - CIRCLE_SOLID_COLOR[1]) * scale
                ),
                int(
                    CIRCLE_SOLID_COLOR[2]
                    + (CIRCLE_GRADIENT_TO_COLOR[2] - CIRCLE_SOLID_COLOR[2]) * scale
                ),
                int(
                    CIRCLE_SOLID_COLOR[3]
                    + (CIRCLE_GRADIENT_TO_COLOR[3] - CIRCLE_SOLID_COLOR[3]) * scale
                ),
            )

            draw.circle(
                center,
                CIRCLE_SOLID_RADIUS + x,
                fill=color,
            )
        img.save("circle.png")

    except Exception as e:
        print(e)
        return


if __name__ == "__main__":
    main()
