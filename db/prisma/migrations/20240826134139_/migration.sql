-- DropIndex
DROP INDEX "Card_text_vector_idx";

-- AlterTable
CREATE SEQUENCE card_index_seq;
ALTER TABLE "Card" ALTER COLUMN "index" SET DEFAULT nextval('card_index_seq');
ALTER SEQUENCE card_index_seq OWNED BY "Card"."index";

-- CreateIndex
CREATE INDEX "Card_text_vector_idx" ON "Card"("text_vector");
