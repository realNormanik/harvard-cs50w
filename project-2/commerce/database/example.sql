-- ============================================================
-- EXAMPLE DATA
-- PostgreSQL / Vercel
-- ============================================================

BEGIN;


-- ============================================================
-- USERS
-- ============================================================

INSERT INTO auctions_user (
    id,
    password,
    last_login,
    is_superuser,
    username,
    first_name,
    last_name,
    email,
    is_staff,
    is_active,
    date_joined,
    watchlist_counter
)
VALUES
(
    1,
    'pbkdf2_sha256$600000$example$NM3mC9boABgLTl2uIwgt0x5awBSmVkt0hdsdqcbt1cY=',
    NULL,
    TRUE,
    'example',
    'Example',
    'User',
    'example@example.com',
    TRUE,
    TRUE,
    '2026-08-18 18:05:00',
    0
),
(
    2,
    'pbkdf2_sha256$600000$example$NM3mC9boABgLTl2uIwgt0x5awBSmVkt0hdsdqcbt1cY=',
    NULL,
    FALSE,
    'user',
    'Example',
    'User',
    'user@example.com',
    FALSE,
    TRUE,
    '2026-08-18 18:06:00',
    3
)
ON CONFLICT (id) DO NOTHING;


-- ============================================================
-- AUCTION LISTINGS
-- ============================================================

INSERT INTO auctions_auctionlisting (
    id,
    user_id,
    title,
    description,
    price,
    starting_bid,
    category,
    image,
    bid_counter,
    created_at,
    active,
    winner
)
VALUES
(
    1,
    1,
    'New Pepe The Frog Meme Men''s T Shirt Happy Pepe Black',
    'The 100% cotton men''s classic tee will help you land a more structured look. It sits nicely, maintains sharp lines around the edges, and goes perfectly with layered streetwear outfits. Plus, it''s extra trendy now!

• 100% cotton
• Sport Grey is 90% cotton, 10% polyester
• Ash Grey is 99% cotton, 1% polyester
• Heather colors are 50% cotton, 50% polyester
• Fabric weight: 5.0–5.3 oz/yd² (170-180 g/m²)
• Open-end yarn
• Tubular fabric
• Taped neck and shoulders
• Double seam at sleeves and bottom hem
• Blank product sourced from Honduras, Nicaragua, Haiti, Dominican Republic, Bangladesh, Mexico

This product is made especially for you as soon as you place an order, which is why it takes us a bit longer to deliver it to you. Making products on demand instead of in bulk helps reduce overproduction, so thank you for making thoughtful purchasing decisions!',
    99.00,
    69.00,
    'Merch',
    'https://fl0bg7voit1klxrh.public.blob.vercel-storage.com/commerce/auctions/OA9dl5Xayf-black.webp',
    1,
    '2026-08-18 18:10:00',
    TRUE,
    NULL
),
(
    2,
    1,
    'New Pepe The Frog Meme Men''s T Shirt Happy Pepe White',
    'The 100% cotton men''s classic tee will help you land a more structured look. It sits nicely, maintains sharp lines around the edges, and goes perfectly with layered streetwear outfits. Plus, it''s extra trendy now!

• 100% cotton
• Sport Grey is 90% cotton, 10% polyester
• Ash Grey is 99% cotton, 1% polyester
• Heather colors are 50% cotton, 50% polyester
• Fabric weight: 5.0–5.3 oz/yd² (170-180 g/m²)
• Open-end yarn
• Tubular fabric
• Taped neck and shoulders
• Double seam at sleeves and bottom hem
• Blank product sourced from Honduras, Nicaragua, Haiti, Dominican Republic, Bangladesh, Mexico

This product is made especially for you as soon as you place an order, which is why it takes us a bit longer to deliver it to you. Making products on demand instead of in bulk helps reduce overproduction, so thank you for making thoughtful purchasing decisions!',
    99.00,
    69.00,
    'Merch',
    'https://fl0bg7voit1klxrh.public.blob.vercel-storage.com/commerce/auctions/OA9dl5Xayf-white.webp',
    1,
    '2026-08-18 18:15:00',
    TRUE,
    NULL
),
(
    3,
    1,
    'New Pepe The Frog Meme Men''s T Shirt Love Pepe Black',
    'The 100% cotton men''s classic tee will help you land a more structured look. It sits nicely, maintains sharp lines around the edges, and goes perfectly with layered streetwear outfits. Plus, it''s extra trendy now!

• 100% cotton
• Sport Grey is 90% cotton, 10% polyester
• Ash Grey is 99% cotton, 1% polyester
• Heather colors are 50% cotton, 50% polyester
• Fabric weight: 5.0–5.3 oz/yd² (170-180 g/m²)
• Open-end yarn
• Tubular fabric
• Taped neck and shoulders
• Double seam at sleeves and bottom hem
• Blank product sourced from Honduras, Nicaragua, Haiti, Dominican Republic, Bangladesh, Mexico

This product is made especially for you as soon as you place an order, which is why it takes us a bit longer to deliver it to you. Making products on demand instead of in bulk helps reduce overproduction, so thank you for making thoughtful purchasing decisions!',
    99.00,
    69.00,
    'Merch',
    'https://fl0bg7voit1klxrh.public.blob.vercel-storage.com/commerce/auctions/JVh6U4pfLw-black.webp',
    1,
    '2026-08-18 18:20:00',
    TRUE,
    NULL
),
(
    4,
    1,
    'New Pepe The Frog Meme Men''s T Shirt Love Pepe White',
    'The 100% cotton men''s classic tee will help you land a more structured look. It sits nicely, maintains sharp lines around the edges, and goes perfectly with layered streetwear outfits. Plus, it''s extra trendy now!

• 100% cotton
• Sport Grey is 90% cotton, 10% polyester
• Ash Grey is 99% cotton, 1% polyester
• Heather colors are 50% cotton, 50% polyester
• Fabric weight: 5.0–5.3 oz/yd² (170-180 g/m²)
• Open-end yarn
• Tubular fabric
• Taped neck and shoulders
• Double seam at sleeves and bottom hem
• Blank product sourced from Honduras, Nicaragua, Haiti, Dominican Republic, Bangladesh, Mexico

This product is made especially for you as soon as you place an order, which is why it takes us a bit longer to deliver it to you. Making products on demand instead of in bulk helps reduce overproduction, so thank you for making thoughtful purchasing decisions!',
    99.00,
    69.00,
    'Merch',
    'https://fl0bg7voit1klxrh.public.blob.vercel-storage.com/commerce/auctions/JVh6U4pfLw-white.webp',
    1,
    '2026-08-18 18:25:00',
    TRUE,
    NULL
),
(
    5,
    1,
    'New Pepe the Frog Meme Men''s T Shirt Classic Pepe Black',
    'The 100% cotton men''s classic tee will help you land a more structured look. It sits nicely, maintains sharp lines around the edges, and goes perfectly with layered streetwear outfits. Plus, it''s extra trendy now!

• 100% cotton
• Sport Grey is 90% cotton, 10% polyester
• Ash Grey is 99% cotton, 1% polyester
• Heather colors are 50% cotton, 50% polyester
• Fabric weight: 5.0–5.3 oz/yd² (170-180 g/m²)
• Open-end yarn
• Tubular fabric
• Taped neck and shoulders
• Double seam at sleeves and bottom hem
• Blank product sourced from Honduras, Nicaragua, Haiti, Dominican Republic, Bangladesh, Mexico

This product is made especially for you as soon as you place an order, which is why it takes us a bit longer to deliver it to you. Making products on demand instead of in bulk helps reduce overproduction, so thank you for making thoughtful purchasing decisions!',
    99.00,
    69.00,
    'Merch',
    'https://fl0bg7voit1klxrh.public.blob.vercel-storage.com/commerce/auctions/tKRe88UyX1-black.webp',
    1,
    '2026-08-18 18:30:00',
    TRUE,
    NULL
),
(
    6,
    1,
    'New Pepe the Frog Meme Men''s T Shirt Classic Pepe White',
    'The 100% cotton men''s classic tee will help you land a more structured look. It sits nicely, maintains sharp lines around the edges, and goes perfectly with layered streetwear outfits. Plus, it''s extra trendy now!

• 100% cotton
• Sport Grey is 90% cotton, 10% polyester
• Ash Grey is 99% cotton, 1% polyester
• Heather colors are 50% cotton, 50% polyester
• Fabric weight: 5.0–5.3 oz/yd² (170-180 g/m²)
• Open-end yarn
• Tubular fabric
• Taped neck and shoulders
• Double seam at sleeves and bottom hem
• Blank product sourced from Honduras, Nicaragua, Haiti, Dominican Republic, Bangladesh, Mexico

This product is made especially for you as soon as you place an order, which is why it takes us a bit longer to deliver it to you. Making products on demand instead of in bulk helps reduce overproduction, so thank you for making thoughtful purchasing decisions!',
    99.00,
    69.00,
    'Merch',
    'https://fl0bg7voit1klxrh.public.blob.vercel-storage.com/commerce/auctions/tKRe88UyX1-white.webp',
    1,
    '2026-08-18 18:35:00',
    TRUE,
    NULL
),
(
    7,
    1,
    'Pepe The Frog Meme Coffee/Tea Mug White',
    'Whether you''re drinking your morning coffee, evening tea, or something in between—this mug''s for you! It''s sturdy and glossy with a vivid print that''ll withstand the microwave and dishwasher.

• Ceramic
• 11 oz mug dimensions: 3.8″ (9.6 cm) in height, 3.2″ (8.2 cm) in diameter
• Lead and BPA-free material
• Dishwasher and microwave safe

This product is made especially for you as soon as you place an order, which is why it takes us a bit longer to deliver it to you. Making products on demand instead of in bulk helps reduce overproduction, so thank you for making thoughtful purchasing decisions!',
    59.00,
    39.00,
    'Merch',
    'https://fl0bg7voit1klxrh.public.blob.vercel-storage.com/commerce/auctions/w22uGNAzzh.webp',
    1,
    '2026-08-18 18:40:00',
    TRUE,
    NULL
)
ON CONFLICT (id) DO NOTHING;


-- ============================================================
-- COMMENTS
-- ============================================================

INSERT INTO auctions_comment (
    id,
    user_id,
    text,
    created_at,
    auction_id,
    image
)
VALUES
(
    1,
    2,
    'Is this T-shirt available in other sizes?',
    '2026-08-18 18:45:00',
    1,
    NULL
),
(
    2,
    2,
    'The black Happy Pepe design looks great.',
    '2026-08-18 18:46:00',
    1,
    NULL
),
(
    3,
    2,
    'Is the white version made from the same cotton fabric?',
    '2026-08-18 18:47:00',
    2,
    NULL
),
(
    4,
    2,
    'Yes, it uses the same product specification.',
    '2026-08-18 18:48:00',
    2,
    NULL
),
(
    5,
    2,
    'Got my order today and got a free pin as a gift, super nice surprise!',
    '2026-08-18 18:50:00',
    1,
    'https://fl0bg7voit1klxrh.public.blob.vercel-storage.com/commerce/comments/fQQxduthop.webp'
)
ON CONFLICT (id) DO NOTHING;


-- ============================================================
-- WATCHLIST
-- ============================================================

INSERT INTO auctions_user_watchlist (
    id,
    user_id,
    auctionlisting_id
)
VALUES
(
    1,
    2,
    1
),
(
    2,
    2,
    3
),
(
    3,
    2,
    5
)
ON CONFLICT (id) DO NOTHING;


COMMIT;