-- count how many products each shop has
  select s.name as shop,
         count(*) as count
    from shop s,
         product p
   where s.id = p.shop_id
group by shop
order by count desc
