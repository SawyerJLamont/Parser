export interface ConjugationItem {
  Word: {
    // Dictionary form information
    dictionary: {
      kanji: string
      hiragana: string
    }
    // Word metadata
    definition: string
    type: WordType
  }
  // Conjugation forms
  "Present Affirmative": {
    kanji: string
    hiragana: string
  }
  "Present Negative": {
    kanji: string
    hiragana: string
  }
  "Past Affirmative": {
    kanji: string
    hiragana: string
  }
  "Past Negative": {
    kanji: string
    hiragana: string
  }
  "Te Form": {
    kanji: string
    hiragana: string
  } | null
}

export type WritingSystem = "kanji" | "hiragana"
export type VerbForm = "dictionary" | "masu"
export type WordType =
  | "verb-ru"
  | "verb-u"
  | "verb-irregular"
  | "noun"
  | "adjective-i"
  | "adjective-na"
  | "adverb"
  | "particle"
  | "expression"

// Restructured conjugation data with improved organization
export const conjugationData: ConjugationItem[] = [
]