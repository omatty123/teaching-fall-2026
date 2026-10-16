# “Back-Water Blues” timing

Recording: Bessie Smith, voice; James P. Johnson, piano, February 17, 1927. The page uses https://www.youtube.com/watch?v=4EZ7mNG7tfM (197.60 seconds).

## Musical timing

The starting reference is the Jazz Audio-Aligned Harmony (JAAH) dataset’s manually annotated beats for this performance, catalogued there as “Black Water Blues”: https://github.com/MTG/JAAH/blob/6fec3f6dd1d60c21cf9af855ea173be38e6d7243/annotations/black_water_blues.json . The current repository annotation was used, rather than the older documentation copy, which contains missing beat entries.

The reference identifies a two-bar introduction and seven twelve-bar vocal choruses. The final beat after the seventh chorus belongs to the ending. Each displayed verse contains 48 beats, grouped into twelve bars of four beats. The display does not impose the separate guitar demo’s chord sequence on Johnson’s accompaniment.

On October 16, 2026, the reference was aligned to the exact YouTube audio. Pitch-class comparison against JAAH’s reference chroma established recording correspondence. Low/mid-register spectral-flux attacks then fitted the beat clock (reference time × 1.0018 − 0.080 seconds) and refined individual beats within 0.140 seconds of that prediction. Median absolute refinement was 0.025 seconds; 95th percentile was 0.098 seconds. These are alignment adjustments, not an independently measured error bound. All seven verse plots were inspected against the detected attacks. This is source-supported computational alignment, not a claim of a musician’s manual transcription or sample-accurate timing.

First-verse bar starts in the embedded video, seconds:
5.044, 7.553, 9.873, 12.107, 14.547, 17.036, 19.411, 21.636, 23.936, 26.315, 28.650, 31.020. The next verse begins at 33.384.

All verse starts: 5.044, 33.384, 61.256, 88.564, 115.213, 142.327, 169.500. The last chorus ends at 196.234; the recording ends at 197.600.

## Voice and playback

Existing word-derived vocal phrase timestamps are retained as approximate vocal indicators only. They do not determine bar boundaries. Smith can begin a lyric before the corresponding four-bar group. The lyric highlight and bar highlight remain independent.

The display follows the YouTube media clock directly, including pause, seek and slower playback. Verse selection starts at the first musical bar, so it can omit a vocal lead-in. Play the recording normally to hear those lead-ins. Browser, output-device and Bluetooth latency can affect perceived synchronization.
