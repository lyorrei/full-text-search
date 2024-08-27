-- AlterTable
ALTER TABLE "Card" ADD COLUMN "text_vector" TSVECTOR
  GENERATED ALWAYS AS
    (to_tsvector('english', coalesce(text, '')))
  STORED;

-- CreateIndex
CREATE INDEX "Card_text_vector_idx" ON "Card" USING GIN ("text_vector");